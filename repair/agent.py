import json
import os

from dotenv import load_dotenv
from google import genai

from .rag_service import retrieve_relevant_knowledge
from collection.services import find_nearest_center


# Load environment variables
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

load_dotenv(os.path.join(BASE_DIR, ".env"))


# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def search_repair_knowledge(category, description):
    """
    Agent tool:
    Searches EcoRepair's repair knowledge base
    for information relevant to the user's problem.
    """

    results = retrieve_relevant_knowledge(
        category,
        description
    )

    return [
        {
            "id": result["item"]["id"],
            "problem": result["item"]["problem"],
            "possible_causes": result["item"]["possible_causes"],
            "diagnostic_clues": result["item"]["diagnostic_clues"],
            "repairability": result["item"]["repairability"],
            "difficulty": result["item"]["difficulty"],
            "repair_guidance": result["item"]["repair_guidance"],
            "safety": result["item"]["safety"],
            "similarity": round(result["similarity"], 3)
        }
        for result in results
    ]


def find_collection_center(category, latitude, longitude):
    """
    Agent tool:
    Finds the nearest collection center that accepts
    the user's electronic item category.
    """

    result = find_nearest_center(
        category,
        latitude,
        longitude
    )

    if result is None:
        return {
            "found": False,
            "message": "No suitable collection center was found."
        }

    return {
        "found": True,
        **result
    }


def run_agent(
    category,
    description,
    latitude=None,
    longitude=None
):
    """
    Gemini agent that can use the repair knowledge tool
    and collection-center tool.
    """

    search_tool = {
        "name": "search_repair_knowledge",
        "description": (
            "Search EcoRepair's repair knowledge base for relevant "
            "repair problems, causes, diagnostic clues, repairability, "
            "difficulty, safety information, and repair guidance."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The device category."
                },
                "description": {
                    "type": "string",
                    "description": "The user's reported problem."
                }
            },
            "required": [
                "category",
                "description"
            ]
        }
    }

    collection_tool = {
        "name": "find_collection_center",
        "description": (
            "Find the nearest e-waste collection center "
            "for the user's device category using their "
            "latitude and longitude."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The user's electronic device category."
                },
                "latitude": {
                    "type": "number",
                    "description": "The user's latitude."
                },
                "longitude": {
                    "type": "number",
                    "description": "The user's longitude."
                }
            },
            "required": [
                "category",
                "latitude",
                "longitude"
            ]
        }
    }

    prompt = f"""
You are the EcoRepair AI agent.

Device category:
{category}

User problem:
{description}

User latitude:
{latitude}

User longitude:
{longitude}

Your job is to determine whether the user's electronic device
problem is repairable, not economical to repair, or uncertain.

IMPORTANT RULES:

1. Use the search_repair_knowledge tool to obtain information
   from EcoRepair's repair knowledge base.

2. The EcoRepair knowledge base is the ONLY source you may use
   for technical diagnosis.

3. Do NOT use your general knowledge to fill gaps in the
   knowledge base.

4. If the retrieved knowledge does not clearly relate to the
   user's actual problem, the result MUST be "uncertain".

5. If the evidence is insufficient, do NOT guess a cause,
   repairability, difficulty, or repair procedure.

6. Only provide a repair guide when the retrieved evidence
   directly supports it.

7. Use the find_collection_center tool only when:
   - the evidence indicates that the item is not economical
     to repair
   - latitude and longitude are available

8. Do not use the collection center tool if location information
   is unavailable.

9. Never invent technical information.

After using the tools, provide the final result.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "tools": [
                {
                    "function_declarations": [
                        search_tool,
                        collection_tool
                    ]
                }
            ]
        }
    )

    # --------------------------------------------------
    # Agent requested a tool
    # --------------------------------------------------

    if response.function_calls:

        function_call = response.function_calls[0]

        # --------------------------------------------------
        # Repair knowledge tool
        # --------------------------------------------------

        if function_call.name == "search_repair_knowledge":

            args = function_call.args

            tool_result = search_repair_knowledge(
                args["category"],
                args["description"]
            )

            # If nothing useful was retrieved, do not allow
            # Gemini to use its own knowledge.
            if not tool_result:
                return {
                    "verdict": "uncertain",
                    "reason": (
                        "The EcoRepair knowledge base does not contain "
                        "enough information about this problem to make "
                        "a reliable repair assessment."
                    ),
                    "difficulty": None,
                    "repair_guide": None,
                    "confidence": 0
                }

            # --------------------------------------------------
            # Send retrieved evidence back to Gemini
            # --------------------------------------------------

            tool_prompt = f"""
You are the EcoRepair AI agent.

Device category:
{category}

User problem:
{description}

The EcoRepair repair knowledge base returned the following evidence:

{json.dumps(tool_result, indent=2)}

IMPORTANT GROUNDING RULE:

You MUST base your answer ONLY on the retrieved EcoRepair
knowledge shown above.

Do NOT use general world knowledge.

Do NOT infer a technical cause that is not supported by
the retrieved evidence.

Do NOT assume that a similar device problem is the same
as the user's problem.

For example, if the user reports screen flickering but
the retrieved knowledge only discusses overheating or
charging, the correct result is "uncertain".

If the retrieved evidence does not clearly address the
user's actual problem:

- verdict = "uncertain"
- difficulty = null
- repair_guide = null
- confidence = 0

Return ONLY valid JSON with exactly these fields:

{{
    "verdict": "repairable" | "not_economical" | "uncertain",
    "reason": "short explanation",
    "difficulty": "easy" | "moderate" | "professional" | null,
    "repair_guide": "practical guidance" | null,
    "confidence": number
}}
"""

            try:

                final_response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=tool_prompt
                )

            except Exception:

                return {
                    "verdict": "uncertain",
                    "reason": (
                        "The repair knowledge was retrieved, but the AI "
                        "could not complete the final diagnosis."
                    ),
                    "difficulty": None,
                    "repair_guide": None,
                    "confidence": 0
                }

            text = final_response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            try:
                return json.loads(text)

            except json.JSONDecodeError:

                return {
                    "verdict": "uncertain",
                    "reason": (
                        "The AI returned an invalid diagnosis format."
                    ),
                    "difficulty": None,
                    "repair_guide": None,
                    "confidence": 0
                }

        # --------------------------------------------------
        # Collection center tool
        # --------------------------------------------------

        elif function_call.name == "find_collection_center":

            args = function_call.args

            tool_result = find_collection_center(
                args["category"],
                args["latitude"],
                args["longitude"]
            )

            final_prompt = f"""
You are the EcoRepair AI agent.

The user reported:

Device category:
{category}

Problem:
{description}

The collection-center tool returned:

{json.dumps(tool_result, indent=2)}

Provide the final result.

Return ONLY valid JSON with exactly these fields:

{{
    "verdict": "repairable" | "not_economical" | "uncertain",
    "reason": "short explanation",
    "difficulty": "easy" | "moderate" | "professional" | null,
    "repair_guide": "practical guidance" | null,
    "confidence": number,
    "collection_center": object | null
}}

If a collection center was found, include it in
"collection_center".

Do not invent information.
"""

            try:

                final_response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=final_prompt
                )

            except Exception:

                return {
                    "verdict": "uncertain",
                    "reason": (
                        "The collection center was found, but the AI "
                        "could not complete the final diagnosis."
                    ),
                    "difficulty": None,
                    "repair_guide": None,
                    "confidence": 0,
                    "collection_center": tool_result
                }

            text = final_response.text.strip()

            if text.startswith("```"):
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

            try:
                return json.loads(text)

            except json.JSONDecodeError:

                return {
                    "verdict": "uncertain",
                    "reason": (
                        "The AI returned an invalid diagnosis format."
                    ),
                    "difficulty": None,
                    "repair_guide": None,
                    "confidence": 0,
                    "collection_center": tool_result
                }

    # --------------------------------------------------
    # No tool was needed
    # --------------------------------------------------

    return {
        "verdict": "uncertain",
        "reason": (
            "There is not enough information to make "
            "a reliable diagnosis."
        ),
        "difficulty": None,
        "repair_guide": None,
        "confidence": 0
    }
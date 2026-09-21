import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables
load_dotenv(BASE_DIR / ".env")


# Gemini setup
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Knowledge files
KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "repair_knowledge.json"
EMBEDDINGS_FILE = BASE_DIR / "knowledge" / "repair_embeddings.json"
# --------------------------------------------------
# Load repair knowledge
# --------------------------------------------------


KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "repair_knowledge.json"


with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
    KNOWLEDGE_BASE = json.load(file)


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------

def create_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


# --------------------------------------------------
# Simple cosine similarity
# --------------------------------------------------

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = sum(a * a for a in vector_a) ** 0.5
    magnitude_b = sum(b * b for b in vector_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


# --------------------------------------------------
# Create searchable text for each knowledge item
# --------------------------------------------------

def knowledge_to_text(item):
    return f"""
Device category: {item['category']}

Problem:
{item['problem']}

Possible causes:
{', '.join(item['possible_causes'])}

Diagnostic clues:
{', '.join(item['diagnostic_clues'])}

Repairability:
{item['repairability']}

Difficulty:
{item['difficulty']}

Repair guidance:
{item['repair_guidance']}

Safety:
{item['safety']}
"""

def build_knowledge_embeddings():
    """
    Create embeddings for all knowledge entries once
    and save them locally.
    """

    embeddings = {}

    for item in KNOWLEDGE_BASE:
        text = knowledge_to_text(item)

        print(f"Creating embedding for: {item['id']}")

        embeddings[item["id"]] = create_embedding(text)

    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(embeddings, file)

    print(f"Saved embeddings to {EMBEDDINGS_FILE}")


def load_knowledge_embeddings():
    """
    Load previously generated knowledge embeddings.
    """

    if not EMBEDDINGS_FILE.exists():
        return None

    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)    
# --------------------------------------------------
# Retrieve relevant knowledge
# --------------------------------------------------

def retrieve_relevant_knowledge(category, description, top_k=3):

    query = f"""
Device category: {category}

User reported problem:
{description}
"""

    query_embedding = create_embedding(query)

    knowledge_embeddings = load_knowledge_embeddings()

    if knowledge_embeddings is None:
        raise FileNotFoundError(
            "repair_embeddings.json not found. "
            "Run build_knowledge_embeddings() first."
        )

    results = []

    for item in KNOWLEDGE_BASE:

        if category != "other" and item["category"] != category:
            continue

        embedding = knowledge_embeddings[item["id"]]

        similarity = cosine_similarity(
            query_embedding,
            embedding
        )

        results.append({
            "item": item,
            "similarity": similarity
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]


def generate_diagnosis(category, description, retrieved_results):

    evidence = []

    for result in retrieved_results:
        item = result["item"]

        evidence.append({
            "problem": item["problem"],
            "possible_causes": item["possible_causes"],
            "diagnostic_clues": item["diagnostic_clues"],
            "repairability": item["repairability"],
            "difficulty": item["difficulty"],
            "repair_guidance": item["repair_guidance"],
            "safety": item["safety"],
            "similarity": round(result["similarity"], 3)
        })

    prompt = f"""
You are EcoRepair's repair advisory AI.

Your job is to analyze an electronic or household appliance problem
using ONLY the retrieved repair knowledge provided below.

User's device category:
{category}

User's reported problem:
{description}

Retrieved repair knowledge:
{json.dumps(evidence, indent=2)}

Rules:

1. Use the retrieved knowledge as evidence.
2. You may reason about the symptoms and connect related clues.
3. Do NOT invent a specific fault when the evidence does not support it.
4. If the evidence is insufficient, return "uncertain".
5. Do not claim that a repair is definitely safe.
6. Electrical, battery, refrigerant, or internal hardware repairs should
   generally be classified as professional repairs.
7. Return ONLY valid JSON.

The JSON must have exactly these fields:

{{
    "verdict": "repairable" | "not_economical" | "uncertain",
    "reason": "short explanation",
    "difficulty": "easy" | "moderate" | "professional" | null,
    "repair_guide": "practical guidance" | null,
    "confidence": number
}}

Confidence must be between 0 and 1.
"""

    interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt
        )

    text = interaction.output_text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)
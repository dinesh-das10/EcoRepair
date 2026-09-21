# EcoRepair

### AI-Powered Repair Advisory & E-Waste Collection Routing Platform

EcoRepair is a web application that helps users decide whether a faulty electronic device may be worth repairing or should be sent for responsible e-waste disposal.

## 🚀 Live Demo

[Open EcoRepair](https://eco-repair.vercel.app/)

### How it works

1. User selects a device and describes the problem.
2. The **AI Repair Advisor** analyzes the problem using EcoRepair's repair knowledge base.
3. A **RAG (Retrieval-Augmented Generation)** pipeline retrieves relevant repair information such as possible causes, diagnostic clues, repairability, difficulty, safety information, and repair guidance.
4. An **AI agent** uses the retrieved evidence to generate a repair assessment. If the knowledge base does not provide enough relevant evidence, the system returns **Uncertain** instead of guessing.
5. If the device is determined to be not economical to repair and location is available, EcoRepair can use its collection-center tool to find a suitable nearby e-waste collection center.
6. The recommended center is displayed on an interactive map.

### 🤖 AI Implementation

EcoRepair combines **RAG and agentic AI** to make the repair advisor more grounded and reliable.

**RAG (Retrieval-Augmented Generation):**

* Repair information is stored in a structured knowledge base.
* User descriptions are converted into embeddings.
* Relevant repair cases are retrieved using semantic similarity.
* The retrieved evidence is provided to the AI before generating the diagnosis.
* If relevant evidence is unavailable, the system returns an **uncertain** result rather than relying on unsupported assumptions.

**Agentic AI:**

* The AI agent can decide when it needs information from the repair knowledge tool.
* It can also use the e-waste collection-center tool when a device is not economical to repair and location information is available.
* This allows the system to combine **information retrieval, reasoning, and tool usage** rather than relying only on a fixed rule-based response.

### Tech Stack

* **Frontend:** React, Vite, Leaflet
* **Backend:** Django, Django REST Framework
* **AI/NLP:** Python, Google Gemini, RAG, Embeddings
* **Database:** SQLite
* **Maps:** OpenStreetMap

### Project Structure

```text
EcoRepair/
├── backend/       # Django configuration
├── repair/        # Repair advisor, RAG & AI agent
├── collection/    # E-waste collection routing
├── knowledge/     # Repair knowledge base & embeddings
├── frontend/      # React application
└── manage.py
```

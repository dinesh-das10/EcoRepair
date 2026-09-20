# EcoRepair

### AI-Powered Repair Advisory & E-Waste Collection Routing Platform

EcoRepair is a web application that helps users decide whether a faulty electronic device may be worth repairing or should be sent for responsible e-waste disposal.

## 🚀 Live Demo

[Open EcoRepair](https://ecorepair-frontend.onrender.com)

### How it works

1. User selects a device and describes the problem.
2. The Repair Advisor matches the description with known fault patterns using **TF-IDF and Cosine Similarity**.
3. The system provides a repair recommendation and basic guidance.
4. If repair is not economical, EcoRepair finds a suitable nearby e-waste collection center.
5. The recommended center is displayed on an interactive map.

### Tech Stack

* **Frontend:** React, Vite, Leaflet
* **Backend:** Django, Django REST Framework
* **AI/NLP:** Python, scikit-learn
* **Database:** SQLite
* **Maps:** OpenStreetMap

### Project Structure

```text
EcoRepair/
├── backend/       # Django configuration
├── repair/        # Repair advisor & AI logic
├── collection/    # E-waste routing
├── frontend/      # React application
└── manage.py
```


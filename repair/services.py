from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import FaultPattern


def check_repairability(category, description):
    """
    Compare the user's problem description with known fault patterns
    for the selected category.
    """

    faults = list(
        FaultPattern.objects.filter(category=category)
    )

    # No known patterns for this category
    if not faults:
        return {
            "verdict": "uncertain",
            "reason": "We don't have enough information about this type of item yet.",
            "difficulty": None,
            "repair_guide": None,
            "confidence": 0,
        }

    # Extract known symptoms
    symptoms = [fault.symptom for fault in faults]

    # Add the user's description at the end
    texts = symptoms + [description]

    # Convert text into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compare user's description with every known symptom
    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    # Find the most similar fault pattern
    best_index = similarities.argmax()
    best_score = float(similarities[best_index])

    best_fault = faults[best_index]

    # Confidence threshold
    if best_score < 0.25:
        return {
            "verdict": "uncertain",
            "reason": (
                "Your description does not closely match "
                "any known fault pattern in our database."
            ),
            "difficulty": None,
            "repair_guide": None,
            "confidence": round(best_score, 2),
        }

    return {
        "verdict": best_fault.verdict,
        "reason": best_fault.reason,
        "difficulty": best_fault.difficulty,
        "repair_guide": best_fault.repair_guide,
        "confidence": round(best_score, 2),
    }
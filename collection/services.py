from math import radians, sin, cos, sqrt, atan2

from .models import CollectionCenter


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographic coordinates
    using the Haversine formula.

    Returns distance in kilometers.
    """

    earth_radius = 6371

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def find_nearest_center(category, user_latitude, user_longitude):
    """
    Find the nearest collection center that accepts
    the user's electronic item category.
    """

    centers = CollectionCenter.objects.all()

    suitable_centers = []

    for center in centers:

        if category not in center.accepted_categories:
            continue

        distance = calculate_distance(
            user_latitude,
            user_longitude,
            center.latitude,
            center.longitude,
        )

        suitable_centers.append({
            "center": center,
            "distance": distance,
        })

    if not suitable_centers:
        return None

    suitable_centers.sort(
        key=lambda item: item["distance"]
    )

    nearest = suitable_centers[0]

    center = nearest["center"]

    return {
        "name": center.name,
        "address": center.address,
        "distance_km": round(nearest["distance"], 2),
        "accepted_categories": center.accepted_categories,
        "operating_info": center.operating_info,
        "latitude": center.latitude,
        "longitude": center.longitude,
    }
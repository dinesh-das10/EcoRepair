from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import find_nearest_center


@api_view(["POST"])
def find_center(request):
    category = request.data.get("category")
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if not category or latitude is None or longitude is None:
        return Response(
            {"error": "Category, latitude and longitude are required."},
            status=400
        )

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return Response(
            {"error": "Latitude and longitude must be numbers."},
            status=400
        )

    center = find_nearest_center(
        category,
        latitude,
        longitude
    )

    if not center:
        return Response(
            {"message": "No suitable e-waste collection center found."},
            status=404
        )

    return Response(center)
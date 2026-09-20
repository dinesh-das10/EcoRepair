from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import check_repairability
from .flow import process_item


@api_view(["POST"])
def repair_check(request):
    category = request.data.get("category")
    description = request.data.get("description")

    if not category or not description:
        return Response(
            {"error": "Category and description are required."},
            status=400
        )

    result = check_repairability(
        category,
        description
    )

    return Response(result)


@api_view(["POST"])
def process_item_api(request):
    category = request.data.get("category")
    description = request.data.get("description")
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if not category or not description:
        return Response(
            {"error": "Category and description are required."},
            status=400
        )

    if latitude is not None and longitude is not None:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response(
                {"error": "Latitude and longitude must be numbers."},
                status=400
            )

    result = process_item(
        category,
        description,
        latitude,
        longitude
    )

    return Response(result)
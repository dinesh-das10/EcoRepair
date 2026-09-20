from .services import check_repairability
from collection.services import find_nearest_center


def process_item(category, description, latitude=None, longitude=None):
    repair_result = check_repairability(
        category,
        description
    )

    # If the item is not economical to repair,
    # find a suitable e-waste collection center.
    if (
        repair_result["verdict"] == "not_economical"
        and latitude is not None
        and longitude is not None
    ):
        center = find_nearest_center(
            category,
            latitude,
            longitude
        )

        repair_result["collection_center"] = center

    return repair_result
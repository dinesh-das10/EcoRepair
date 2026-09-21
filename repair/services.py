from .agent import run_agent


def check_repairability(
    category,
    description,
    latitude=None,
    longitude=None
):
    return run_agent(
        category,
        description,
        latitude,
        longitude
    )
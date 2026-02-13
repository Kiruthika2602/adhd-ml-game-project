def calculate_hyperactivity(shield: dict) -> int:
    """
    Hyperactivity score:
    1 jitter or restlessness event = 1 point
    Maximum capped at 9
    """
    jitter = shield.get("jitter_events", 0) or 0
    restlessness = shield.get("restlessness_events", 0) or 0

    activity = int(jitter) + int(restlessness)
    return min(activity, 9)

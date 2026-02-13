def calculate_inattention(pilot: dict) -> int:
    """
    Inattention score:
    1 omission or distractor error = 1 point
    Maximum capped at 9
    """
    omissions = pilot.get("omissions", 0) or 0
    distractor_errors = pilot.get("distractor_errors", 0) or 0

    errors = int(omissions) + int(distractor_errors)
    return min(errors, 9)

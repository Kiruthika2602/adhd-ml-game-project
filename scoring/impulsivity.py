def calculate_impulsivity(reaction: dict) -> int:
    """
    Impulsivity score:
    1 commission error or premature click = 1 point
    Maximum capped at 9
    """
    commission = reaction.get("commission_errors", 0) or 0
    premature = reaction.get("premature_clicks", 0) or 0

    impulsive = int(commission) + int(premature)
    return min(impulsive, 9)

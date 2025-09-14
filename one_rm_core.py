
"""
Core math for Class Workout 105 helper.
Pure functions so we can reuse in Streamlit and Tkinter apps.
"""
from typing import Dict, List, Sequence, Tuple

def round_to_increment(x: float, increment: float = 5.0) -> float:
    """Round x to the nearest increment (default 5 lb)."""
    if increment <= 0:
        return float(x)
    return float(int(round(float(x) / increment)) * increment)

def class_rule_1rm(weight_lbs: float, add_on_lbs: float = 10.0) -> float:
    """Class rule: 1RM is measured working weight plus a fixed add-on (default +10 lb)."""
    return max(0.0, float(weight_lbs) + float(add_on_lbs))

def epley_1rm(weight_lbs: float, reps: int) -> float:
    """Epley (1985): 1RM = w * (1 + reps/30). Reasonable for 1-10 reps."""
    r = max(1, int(reps))
    return float(weight_lbs) * (1.0 + (r / 30.0))

def brzycki_1rm(weight_lbs: float, reps: int) -> float:
    """Brzycki (1993): 1RM = w * 36 / (37 - reps). Valid-ish for 1-10 reps."""
    r = max(1, int(reps))
    if r >= 37:
        # Out of domain; fall back to weight
        return float(weight_lbs)
    return float(weight_lbs) * 36.0 / (37.0 - r)

def percent_of_1rm(one_rm: float, percent: float) -> float:
    """Return the target load at a given percent of a 1RM."""
    return float(one_rm) * (float(percent) / 100.0)

def plate_math(total_weight: float,
               bar_weight: float = 45.0,
               plate_sizes: Sequence[float] = (45.0, 25.0, 10.0, 5.0)) -> Tuple[List[Tuple[float, int]], float]:
    """
    Compute per-side plates for a given TOTAL barbell weight (including the bar).
    Returns (list of (plate_size, count_per_side), remainder_lbs_per_side).
    Greedy by design (standard gym practice).
    """
    total_weight = float(total_weight)
    bar_weight = float(bar_weight)
    if total_weight < bar_weight:
        return [], total_weight - bar_weight  # negative remainder indicates under the bar weight

    load_total = total_weight - bar_weight
    per_side = load_total / 2.0
    plan: List[Tuple[float, int]] = []
    for p in plate_sizes:
        count = int(per_side // p)
        if count > 0:
            plan.append((float(p), count))
            per_side -= count * p
    remainder = round(per_side, 4)  # leftover per side
    return plan, remainder

def format_plate_plan(plan: List[Tuple[float, int]], remainder_per_side: float) -> str:
    """Human-readable plate plan string like '45×1, 25×1 (per side)'; note remainder if any."""
    if not plan:
        return "—"
    parts = [f"{int(p) if p.is_integer() else p}×{c}" for p, c in plan]
    s = ", ".join(parts) + " (per side)"
    if abs(remainder_per_side) >= 0.01:
        s += f" + remainder {remainder_per_side:.1f} lb"
    return s

import streamlit as st
import pandas as pd
from one_rm_core import (
    round_to_increment, class_rule_1rm, epley_1rm, brzycki_1rm,
    percent_of_1rm, plate_math, format_plate_plan
)

st.set_page_config(page_title="Class Workout 105 — 1RM Helper", layout="centered", initial_sidebar_state="expanded")
# Read default from URL (?inline=1)
qs = st.query_params
default_inline = qs.get("inline", "0") == "1"

st.title("Class Workout 105 — 1 Rep Max Helper")
selected_ex_placeholder = st.empty()
mobile_inputs = st.toggle(
    "Show inputs inline (mobile)",
    value=default_inline,
    key="inline_toggle",
    help="If the sidebar is hidden on a small screen, turn this on to show the inputs below."
)

if st.session_state.get("inline_toggle"):
    st.markdown(
        "<style>@media (max-width: 700px){section[data-testid='stSidebar']{display:none;}}</style>",
        unsafe_allow_html=True
    )
EXERCISES = [
    "Bench Press",
    "Leg Press",
    "Face Pulls",
    "Goblet Squats",
    "Wide Grip Lat Pulldown",
    "Dumbell Incline",
    "Leg Curls",
    "Dumbell Curls",
    "Tricep Pushdown",
    "Dumbell Front Raises",
    "Incline Bench",
    "Seated Row",
    "Dumbell RDL",
    "Hammer Curls",
]

# Which exercises are barbell (eligible for plate math)?
BARBELL = {"Bench Press": True, "Incline Bench": True}

if mobile_inputs:
    with st.container():
        st.markdown("### Inputs")
        # Give inline widgets unique keys to avoid any session clashes
        ex = st.selectbox("Exercise", EXERCISES, index=0, key="ex_inline")
        weight = st.number_input("Measured weight (lbs)", min_value=0.0, step=5.0, value=185.0,
                                 format="%.1f", key="wt_inline")
        reps = st.number_input("Reps performed to max", min_value=1, step=1, value=3, key="reps_inline")
        add_on = st.number_input("Class add-on (+ lbs)", min_value=0.0, step=1.0, value=10.0,
                                 format="%.1f", key="addon_inline")
        percent = st.number_input("Show % of 1RM (e.g., 60 = 60%)", min_value=1.0, max_value=120.0,
                                  step=1.0, value=60.0, format="%.0f", key="pct_inline")
        show_common = st.checkbox("Show common % table (60–100%)", value=True, key="table_inline")
        sled = 0.0
        if ex == "Leg Press":
            sled = st.number_input("Leg press sled weight (lb)", min_value=0.0, step=5.0, value=0.0,
                                   help="Enter your machine's empty sled weight to show plate math.",
                                   key="sled_inline")
else:
    with st.sidebar:
        st.header("Inputs")
        ex = st.selectbox("Exercise", EXERCISES, index=0, key="ex_side")
        weight = st.number_input("Measured weight (lbs)", min_value=0.0, step=5.0, value=185.0,
                                 format="%.1f", key="wt_side")
        reps = st.number_input("Reps performed to max", min_value=1, step=1, value=3, key="reps_side")
        add_on = st.number_input("Class add-on (+ lbs)", min_value=0.0, step=1.0, value=10.0,
                                 format="%.1f", key="addon_side")
        percent = st.number_input("Show % of 1RM (e.g., 60 = 60%)", min_value=1.0, max_value=120.0,
                                  step=1.0, value=60.0, format="%.0f", key="pct_side")
        show_common = st.checkbox("Show common % table (60–100%)", value=True, key="table_side")
        sled = 0.0
        if ex == "Leg Press":
            sled = st.number_input("Leg press sled weight (lb)", min_value=0.0, step=5.0, value=0.0,
                                   help="Enter your machine's empty sled weight to show plate math.",
                                   key="sled_side")
selected_ex_placeholder.markdown(f"## Exercise: {ex}")

st.caption("Class rule uses measured weight **plus** the add-on (ignores reps)."
           " Formula estimates (Epley/Brzycki) use both weight and reps. "
           "All outputs are rounded to the nearest 5 lb.")

# Plate math configuration (includes 2.5 lb plates)
PLATE_SIZES = (45.0, 25.0, 10.0, 5.0, 2.5)

methods = []
# Class rule
one_rm_class = class_rule_1rm(weight, add_on)
methods.append(("Class +{:.0f}".format(add_on), one_rm_class))

# Epley
one_rm_epley = epley_1rm(weight, int(reps))
methods.append(("Epley", one_rm_epley))

# Brzycki
one_rm_brzycki = brzycki_1rm(weight, int(reps))
methods.append(("Brzycki", one_rm_brzycki))

st.subheader("Results")

rows = []
for name, one_rm in methods:
    one_rm_r = round_to_increment(one_rm, 5.0)
    target = percent_of_1rm(one_rm_r, percent)
    target_r = round_to_increment(target, 5.0)

    plate_str = "—"
    if BARBELL.get(ex, False):
        plan, rem = plate_math(target_r, bar_weight=45.0, plate_sizes=PLATE_SIZES)
        plate_str = format_plate_plan(plan, rem)
    elif ex == "Leg Press":
        if sled > 0:
            plan, rem = plate_math(target_r, bar_weight=sled, plate_sizes=PLATE_SIZES)
            plate_str = format_plate_plan(plan, rem)
        else:
            plate_str = "Set sled weight"

    rows.append({
        "Method": name,
        "1RM (rounded)": f"{one_rm_r:.0f} lb",
        f"{int(percent)}% of 1RM": f"{target_r:.0f} lb",
        "Plate Math": plate_str
    })

st.table(pd.DataFrame(rows))

if show_common:
    st.markdown("---")
    st.subheader("Common Percentages Table")
    common_pcts = [60, 65, 70, 75, 80, 85, 90, 100]

    # Build a table per method
    for name, one_rm in methods:
        one_rm_r = round_to_increment(one_rm, 5.0)
        st.markdown(f"**{name} — 1RM {one_rm_r:.0f} lb**")
        data = []
        for p in common_pcts:
            t = round_to_increment(percent_of_1rm(one_rm_r, p), 5.0)
            if BARBELL.get(ex, False):
                plan, rem = plate_math(t, 45.0, PLATE_SIZES)
                plate_str = format_plate_plan(plan, rem)
            elif ex == "Leg Press":
                if sled > 0:
                    plan, rem = plate_math(t, sled, PLATE_SIZES)
                    plate_str = format_plate_plan(plan, rem)
                else:
                    plate_str = "Set sled weight"
            else:
                plate_str = "—"
            data.append({"%": f"{p}%", "Weight": f"{t:.0f} lb", "Plates": plate_str})
        st.table(pd.DataFrame(data))

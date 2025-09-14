
import tkinter as tk
from tkinter import ttk, messagebox
from one_rm_core import (
    round_to_increment, class_rule_1rm, epley_1rm, brzycki_1rm,
    percent_of_1rm, plate_math, format_plate_plan
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
BARBELL = {"Bench Press": True, "Incline Bench": True}

def compute():
    try:
        ex = ex_var.get()
        w = float(weight_var.get())
        r = int(reps_var.get())
        add = float(addon_var.get())
        pct = float(percent_var.get())
    except Exception as e:
        messagebox.showerror("Input error", f"Please check your inputs.\n\n{e}")
        return

    rows = []
    methods = [
        (f"Class +{add:.0f}", class_rule_1rm(w, add)),
        ("Epley", epley_1rm(w, r)),
        ("Brzycki", brzycki_1rm(w, r)),
    ]
    out_lines = []
    for name, orm in methods:
        orm_r = round_to_increment(orm, 5.0)
        tgt = round_to_increment(percent_of_1rm(orm_r, pct), 5.0)
        line = f"{name}: 1RM {orm_r:.0f} lb | {pct:.0f}% -> {tgt:.0f} lb"
        if BARBELL.get(ex, False):
            plan, rem = plate_math(tgt, 45.0, (45.0, 25.0, 10.0, 5.0))
            line += " | Plates: " + format_plate_plan(plan, rem)
        out_lines.append(line)

    result_var.set("\n".join(out_lines))

root = tk.Tk()
root.title("Class Workout 105 — 1RM Helper")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Exercise").grid(column=0, row=0, sticky="w")
ex_var = tk.StringVar(value=EXERCISES[0])
ttk.OptionMenu(frm, ex_var, EXERCISES[0], *EXERCISES).grid(column=1, row=0, sticky="ew")

ttk.Label(frm, text="Measured weight (lb)").grid(column=0, row=1, sticky="w")
weight_var = tk.StringVar(value="185")
ttk.Entry(frm, textvariable=weight_var, width=10).grid(column=1, row=1, sticky="ew")

ttk.Label(frm, text="Reps to max").grid(column=0, row=2, sticky="w")
reps_var = tk.StringVar(value="3")
ttk.Entry(frm, textvariable=reps_var, width=10).grid(column=1, row=2, sticky="ew")

ttk.Label(frm, text="Class add-on (+lb)").grid(column=0, row=3, sticky="w")
addon_var = tk.StringVar(value="10")
ttk.Entry(frm, textvariable=addon_var, width=10).grid(column=1, row=3, sticky="ew")

ttk.Label(frm, text="Percent of 1RM (e.g., 60)").grid(column=0, row=4, sticky="w")
percent_var = tk.StringVar(value="60")
ttk.Entry(frm, textvariable=percent_var, width=10).grid(column=1, row=4, sticky="ew")

ttk.Button(frm, text="Compute", command=compute).grid(column=0, row=5, columnspan=2, pady=(8, 4))

result_var = tk.StringVar(value="")
ttk.Label(frm, textvariable=result_var, justify="left").grid(column=0, row=6, columnspan=2, sticky="w")

for i in range(2):
    frm.grid_columnconfigure(i, weight=1)

root.mainloop()

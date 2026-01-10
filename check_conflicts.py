# check_conflicts.py
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if line.startswith("<<<<<<<") or line.startswith("=======") or line.startswith(">>>>>>>"):
        print(f"Conflict marker found on line {i}: {line.strip()}")

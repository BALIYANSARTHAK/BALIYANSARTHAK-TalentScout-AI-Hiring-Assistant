import re
import os
import pandas as pd
from datetime import datetime

EXIT_KEYWORDS = {"bye", "exit", "quit", "goodbye", "end", "stop", "finish", "thanks", "thank you"}

def is_exit(text: str) -> bool:
    if not text:
        return False
    t = text.lower().strip()
    return any(kw in t for kw in EXIT_KEYWORDS)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[+()\-\s\d]{7,20}$")

def valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email or ""))

def valid_phone(phone: str) -> bool:
    return bool(PHONE_RE.match(phone or ""))

def save_candidate_row(path_csv: str, row: dict):
    cols = ["timestamp","full_name","email","phone","years_experience","desired_position","current_location","tech_stack","notes"]
    df = pd.DataFrame([{
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        **{k: row.get(k, "") for k in cols if k not in ("timestamp",)}
    }])
    if os.path.exists(path_csv):
        df.to_csv(path_csv, mode="a", index=False, header=False)
    else:
        df.to_csv(path_csv, index=False)

def pretty_join(items):
    items = [i for i in (items or []) if str(i).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]

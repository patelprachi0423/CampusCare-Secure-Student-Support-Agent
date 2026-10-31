import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT / "docs" / "student_handbook.txt"
_MEMORY = {}

def demo_students():
    return {
        "STU1001": {"name": "Aarav Shah", "fee_status": "Partially Paid", "fee_due_inr": 25000},
        "STU1002": {"name": "Meera Patel", "fee_status": "Paid", "fee_due_inr": 0},
        "STU1003": {"name": "Rohan Desai", "fee_status": "Pending", "fee_due_inr": 18000},
    }

def get_fee_record(signed_in_student_id, requested_student_id):
    if signed_in_student_id != requested_student_id:
        return {"error": "Access denied. You can only view your own private student record."}
    students = demo_students()
    if requested_student_id not in students:
        return {"error": "Student record not found."}
    return {"student_id": requested_student_id, **students[requested_student_id]}

def search_handbook(query, limit=4):
    if not query or not query.strip() or not HANDBOOK.exists():
        return []
    terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    paragraphs = [p.strip() for p in HANDBOOK.read_text(encoding="utf-8").split("\n\n") if p.strip()]
    scored = []
    for p in paragraphs:
        words = set(re.findall(r"[a-z0-9]+", p.lower()))
        score = len(terms & words)
        if score:
            scored.append((score, {"title": p.splitlines()[0].strip("# ").strip()[:100], "text": p}))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:limit]]

def detect_secret(text):
    if not text:
        return []
    patterns = {
        "password": r"(?i)\b(password|passwd|pwd)\s*[:=]\s*\S+",
        "OTP": r"(?i)\b(otp|one[- ]time password)\s*[:=]?\s*\d{4,8}\b",
        "API key/token": r"(?i)\b(api[_ -]?key|access[_ -]?token|secret[_ -]?key)\s*[:=]\s*[A-Za-z0-9_\-]{8,}",
        "credential phrase": r"(?i)\b(my password is|my otp is)\s+\S+",
    }
    return [label for label, pattern in patterns.items() if re.search(pattern, text)]

def request_sensitive_action(student_id, action, reason):
    return {"approval_id": "APR-" + uuid.uuid4().hex[:6].upper(), "student_id": student_id,
            "action": action, "reason": reason.strip(), "status": "Pending", "result": "not_executed"}

def resolve_approval(item, decision):
    if decision not in {"Approved", "Rejected"}:
        raise ValueError("Decision must be Approved or Rejected.")
    result = item.copy()
    result["status"] = decision
    result["result"] = "approved_demo_only" if decision == "Approved" else "rejected_no_change_executed"
    return result

def save_memory(student_id, text):
    if not text or not text.strip():
        return False, "Please enter a non-empty preference."
    if detect_secret(text):
        return False, "Memory rejected: secret-like content must not be stored."
    _MEMORY.setdefault(student_id, []).append(text.strip())
    return True, "Preference saved for this running session."

def load_memory(student_id):
    return list(_MEMORY.get(student_id, []))

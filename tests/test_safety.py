from src.agent import get_fee_record, detect_secret, request_sensitive_action, resolve_approval, save_memory, load_memory, search_handbook

def test_own_student_record_allowed():
    assert get_fee_record("STU1001", "STU1001")["student_id"] == "STU1001"

def test_other_student_record_blocked():
    result = get_fee_record("STU1001", "STU1002")
    assert "Access denied" in result["error"]

def test_secret_detector():
    assert "password" in detect_secret("password: abc123")
    assert "OTP" in detect_secret("OTP: 123456")

def test_rejection_executes_no_change():
    item = request_sensitive_action("STU1001", "Fee dispute", "Please review")
    assert item["status"] == "Pending"
    assert resolve_approval(item, "Rejected")["result"] == "rejected_no_change_executed"

def test_secret_not_saved():
    ok, _ = save_memory("TEST", "password: abc123")
    assert not ok
    assert load_memory("TEST") == []

def test_handbook_retrieval():
    assert search_handbook("attendance")

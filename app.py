import streamlit as st
from src.agent import demo_students, get_fee_record, search_handbook, detect_secret, request_sensitive_action, resolve_approval, save_memory, load_memory

st.set_page_config(page_title="CampusCare Secure", page_icon="🛡️", layout="wide")
st.title("🛡️ CampusCare Secure Student Support Agent")
st.caption("Educational prototype: privacy, secret detection, and approval controls.")
students = demo_students()
ids = list(students)
current = st.sidebar.selectbox("Demo signed-in student", ids, format_func=lambda x: f"{x} — {students[x]['name']}")
st.sidebar.info("Demo selector only; this is not real authentication.")
t1, t2, t3, t4 = st.tabs(["My fee record", "Student handbook", "Safety checks", "Approval queue"])

with t1:
    st.subheader("Private student fee record")
    target = st.selectbox("Record to view (for testing access control)", ids, index=ids.index(current))
    if st.button("View fee record"):
        result = get_fee_record(current, target)
        if "error" in result: st.error(result["error"])
        else: st.success("Access allowed: your own demo record."); st.json(result)

with t2:
    st.subheader("Search the student handbook")
    query = st.text_input("Search topic", placeholder="attendance, fee payment, scholarship")
    if st.button("Search handbook"):
        matches = search_handbook(query)
        if matches:
            for item in matches:
                st.markdown(f"**{item['title']}**")
                st.write(item["text"])
        else: st.warning("No matching paragraphs found. Try another keyword.")

with t3:
    st.subheader("Secret-like input detection")
    sample = st.text_area("Enter sample text to check (do not enter real passwords or OTPs)")
    if st.button("Check input"):
        found = detect_secret(sample)
        if found: st.error("Potential secret detected: " + ", ".join(found) + ". Do not share or store it.")
        else: st.success("No common secret patterns detected. This check is not perfect.")
    st.divider()
    st.subheader("Safe memory")
    memory = st.text_input("Save a non-sensitive preference", placeholder="prefers concise explanations")
    if st.button("Save memory"):
        ok, msg = save_memory(current, memory)
        (st.success if ok else st.error)(msg)
    st.write("Saved demo memories for this running session:")
    st.json(load_memory(current))

with t4:
    st.subheader("Sensitive action approval")
    action = st.selectbox("Requested action", ["Change contact details", "Submit fee dispute", "Update scholarship application"])
    reason = st.text_area("Reason")
    if st.button("Request approval"):
        item = request_sensitive_action(current, action, reason)
        st.session_state.setdefault("approval_items", []).append(item)
        st.info(f"Request {item['approval_id']} is pending. No change has been executed.")
    for item in st.session_state.get("approval_items", []):
        st.markdown(f"**{item['approval_id']} — {item['action']} — {item['status']}**")
        st.write(item["reason"])
        if item["status"] == "Pending":
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Approve " + item["approval_id"], key="a"+item["approval_id"]):
                    item.update(resolve_approval(item, "Approved"))
                    st.success("Approved in demo only; no external system was changed.")
            with c2:
                if st.button("Reject " + item["approval_id"], key="r"+item["approval_id"]):
                    item.update(resolve_approval(item, "Rejected"))
                    st.warning("Rejected. No change was executed.")
        elif item["status"] == "Rejected": st.warning("Rejected — no change executed.")
        else: st.success("Approved — demo status only.")

# CampusCare Secure Student Support Agent

Educational Streamlit prototype demonstrating student-record privacy, handbook retrieval, secret-like input detection, approval-gated actions, and safe memory.

## Run on Windows
1. Install Python 3.10+.
2. Open Command Prompt in this folder.
3. Run `py -m venv .venv`
4. Run `.venv\Scripts\activate`
5. Run `pip install -r requirements.txt`
6. Run `streamlit run app.py`
7. Open the local URL shown in the terminal.

## Run tests
Run `pytest -q`.

## Demo
- Select a demo student and view their own fee record.
- Try viewing another student's record; access should be denied.
- Search the handbook for attendance, fee payment, scholarship, or technical support.
- Test the secret detector with a sample such as `password: abc123` (never enter real secrets).
- Submit a sensitive action and approve/reject it. Rejection must not execute a change.
- Try saving a password-like string to memory; it should be refused.

## Important
This is a classroom prototype, not a production student-information system. It uses a demo identity selector and sample data. Do not use real student data or credentials. Production use requires institutional authentication, robust role-based access control, secure database design, audit logging, and a real authorized approval workflow.

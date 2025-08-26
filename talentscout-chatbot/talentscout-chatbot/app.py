import os
import json
import streamlit as st
from dotenv import load_dotenv
from typing import List, Dict, Any
from chatbot import generate_questions_for_stack
from utils import valid_email, valid_phone, save_candidate_row, pretty_join, is_exit

load_dotenv()

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="centered")

st.title("🤖 TalentScout — AI Hiring Assistant")
st.caption("Initial technical screening for technology candidates.")

with st.expander("🔒 Data & Privacy", expanded=False):
    st.markdown("""- This demo collects the details you enter to generate tailored technical questions.
- We store candidate records locally in `data/candidates.csv` for demonstration.
- Do **not** enter sensitive data beyond your contact and tech profile.
- By continuing, you consent to this simulated data handling. For production, add encryption, consent flow, and GDPR/DPDP compliance.
""")

# Session state
if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "full_name": "",
        "email": "",
        "phone": "",
        "years_experience": 0.0,
        "desired_position": "",
        "current_location": "",
        "tech_stack": [],
        "notes": ""
    }
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "conversation_over" not in st.session_state:
    st.session_state.conversation_over = False

st.subheader("👤 Candidate Details")
col1, col2 = st.columns(2)
with col1:
    st.session_state.candidate["full_name"] = st.text_input("Full Name *", value=st.session_state.candidate["full_name"])
    st.session_state.candidate["email"] = st.text_input("Email *", value=st.session_state.candidate["email"], help="We'll validate basic format.")
    st.session_state.candidate["phone"] = st.text_input("Phone *", value=st.session_state.candidate["phone"])
    st.session_state.candidate["years_experience"] = st.number_input("Years of Experience *", min_value=0.0, max_value=50.0, step=0.5, value=float(st.session_state.candidate["years_experience"] or 0.0))
with col2:
    st.session_state.candidate["desired_position"] = st.text_input("Desired Position(s) *", value=st.session_state.candidate["desired_position"])
    st.session_state.candidate["current_location"] = st.text_input("Current Location *", value=st.session_state.candidate["current_location"])
    tech_text = st.text_area("Tech Stack (comma-separated) *", value=pretty_join(st.session_state.candidate.get("tech_stack")) or "", placeholder="e.g., Python, Django, SQL, React, AWS")
    st.session_state.candidate["notes"] = st.text_area("Notes (optional)", value=st.session_state.candidate["notes"])

# Parse tech stack
tech_stack_list = [t.strip() for t in tech_text.split(",")] if tech_text else []
st.session_state.candidate["tech_stack"] = [t for t in tech_stack_list if t]

# Validate mandatory fields
def _valid_candidate(c: Dict[str, Any]) -> List[str]:
    errors = []
    if not c["full_name"].strip(): errors.append("Full Name is required.")
    if not valid_email(c["email"]): errors.append("Email format looks invalid.")
    if not valid_phone(c["phone"]): errors.append("Phone format looks invalid.")
    if c["years_experience"] is None or c["years_experience"] < 0: errors.append("Years of Experience must be ≥ 0.")
    if not c["desired_position"].strip(): errors.append("Desired Position is required.")
    if not c["current_location"].strip(): errors.append("Current Location is required.")
    if not c["tech_stack"]: errors.append("Please provide at least one technology in Tech Stack.")
    return errors

st.divider()
st.subheader("🧪 Tech Questions")

colA, colB = st.columns([1,1])
with colA:
    if st.button("Generate Questions"):
        errors = _valid_candidate(st.session_state.candidate)
        if errors:
            st.error("\n".join(f"• {e}" for e in errors))
        else:
            st.session_state.tech_questions = generate_questions_for_stack(st.session_state.candidate["tech_stack"])

with colB:
    if st.button("Save Candidate Record"):
        errors = _valid_candidate(st.session_state.candidate)
        if errors:
            st.error("\n".join(f"• {e}" for e in errors))
        else:
            csv_path = os.path.join("data", "candidates.csv")
            os.makedirs("data", exist_ok=True)
            save_candidate_row(csv_path, {
                **st.session_state.candidate,
                "tech_stack": pretty_join(st.session_state.candidate["tech_stack"])
            })
            st.success("Saved! Record appended to data/candidates.csv")


st.divider()
st.subheader("📂 Saved Candidates")

if st.button("View Saved Candidates"):
    csv_path = os.path.join("data", "candidates.csv")
    if os.path.exists(csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)
        st.dataframe(df)
    else:
        st.warning("No candidates saved yet.")

# Display questions
if st.session_state.tech_questions:
    for tech in st.session_state.tech_questions:
        with st.container(border=True):
            st.markdown(f"**{tech['name']}**")
            for i, q in enumerate(tech["questions"], start=1):
                st.write(f"{i}. {q}")

st.divider()
st.subheader("💬 Chat (Optional)")

st.markdown("""Type to interact with the assistant. Use keywords like **bye**, **exit**, or **stop** to end the conversation.
""")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

user_msg = st.text_input("Your message", key="chat_input")
send = st.button("Send Message", type="primary")

def _bot_reply(user_text: str) -> str:
    if is_exit(user_text):
        st.session_state.conversation_over = True
        return "Thank you for your time! We'll review your details and get back to you with the next steps. ✅"

    lower = (user_text or "").lower()

    if any(k in lower for k in ("name", "email", "phone")) and not st.session_state.candidate["full_name"]:
        return "Please fill the candidate details form above, then I can tailor questions for you."

    if "question" in lower or "interview" in lower:
        return "Click **Generate Questions** above to see tailored questions for your tech stack."

    # Default fallback
    return "Got it! Is there anything else you’d like to share about your experience or projects?"

if send and user_msg.strip():
    st.session_state.chat_log.append(("You", user_msg.strip()))
    st.session_state.chat_log.append(("TalentScout", _bot_reply(user_msg.strip())))
    st.rerun()

for speaker, msg in st.session_state.chat_log[-10:]:
    st.markdown(f"**{speaker}:** {msg}")

if st.session_state.conversation_over:
    st.info("Conversation ended. You can still edit the form or save your record.")

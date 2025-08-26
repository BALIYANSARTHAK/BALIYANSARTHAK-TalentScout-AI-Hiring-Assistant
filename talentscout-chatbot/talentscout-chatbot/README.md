# TalentScout — AI/ML Intern Assignment (Hiring Assistant Chatbot)

An intelligent hiring assistant chatbot for a fictional recruitment agency **TalentScout**. It collects candidate info and generates tailored technical questions based on the tech stack.

## ✨ Features
- Streamlit UI with candidate form (name, email, phone, YOE, position, location, tech stack)
- Tailored **3–5** technical questions per technology (OpenAI-powered with graceful fallback)
- Conversation box with polite, on-purpose responses and exit keywords
- Local data persistence to `data/candidates.csv` (simulated, anonymizable)
- Clear privacy notice and assignment-aligned behavior
- Modular, documented codebase with prompt templates

## 🗂 Project Structure
```
talentscout-chatbot/
│── app.py               # Streamlit UI
│── chatbot.py           # LLM calls + question generation + fallback bank
│── prompts.py           # System + generation prompts
│── utils.py             # Validation, persistence helpers, exit keywords
│── requirements.txt     # Dependencies
│── .env.example         # Sample env file (copy to .env)
│── data/                # Local storage (candidates.csv)
└── README.md
```

## 🚀 Quickstart (Local)
1) **Clone or unzip** this repo  
2) **Create venv (recommended)**
```bash
python -m venv .venv
source .venv/bin/activate   # (Windows) .venv\Scripts\activate
```
3) **Install deps**
```bash
pip install -r requirements.txt
```
4) **Configure API (optional, enables smarter questions)**
- Copy `.env.example` to `.env` and set `OPENAI_API_KEY`
- Optionally change `OPENAI_MODEL` (e.g., `gpt-4o`, `gpt-4o-mini`)

5) **Run**
```bash
streamlit run app.py
```

> Without an API key, the app still works using a curated fallback question bank.

## 🧠 Prompt Design
- **System prompt** enforces role, scope, tone, and exit behavior.
- **Question prompt** requests a strict JSON structure of questions per technology.
- **Fallback prompt** produces minimal JSON lists when a tech is unknown.

See `prompts.py`.

## 🔐 Data Privacy (Simulated)
- This demo stores candidate rows locally in `data/candidates.csv`.
- Do **not** add sensitive info beyond the form fields.
- For production, add: encryption at rest, explicit consent, data retention policies, audit logging, and GDPR/DPDP compliance.

## 🧩 Assignment Mapping
- Greeting & overview: in UI and system prompt
- Info gathering: candidate form
- Tech stack declaration: comma-separated input
- Question generation: LLM or fallback
- Context handling: Streamlit session state, chat box
- Fallback mechanism: curated bank + default replies
- End conversation: exit keywords
- Documentation: this README + clear code
- Deployment: Local ready; easy to push to **Streamlit Community Cloud**

## ☁️ Optional: Deploy on Streamlit Community Cloud
- Push to GitHub
- Add repository on streamlit.io
- Set `OPENAI_API_KEY` as a secret in the app settings
- Click Deploy — share the live URL + a Loom walkthrough

## 🎥 Demo (Loom)
Record a short clip showing:
1. Opening the app, privacy note
2. Filling form with sample candidate details
3. Generating questions for 2–3 techs
4. Saving candidate to CSV
5. Using chat box + ending via 'bye'

## 🧪 Tech Notes
- Uses OpenAI Chat Completions with `response_format` for JSON when available.
- If API unavailable, falls back to a small curated bank and generic builders.
- Clean separation of UI, prompts, and logic for easy grading.

## 📄 License
MIT


## ➕ New: View Saved Candidates
You can now view the demo `candidates.csv` directly in the app under the "View Saved Candidates" section and download it. A `LOOM_SCRIPT.md` file is included with a ready-to-read demo recording script.

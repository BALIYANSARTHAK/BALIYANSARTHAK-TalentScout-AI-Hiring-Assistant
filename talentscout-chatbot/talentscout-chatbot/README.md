🚀 TalentScout — AI Hiring Assistant Chatbot

An intelligent AI-powered hiring assistant that automates candidate screening and generates tailored technical interview questions based on a candidate’s tech stack.

💡 Built to reduce manual screening effort and enable faster, smarter hiring decisions.

🎯 Problem

Recruiters spend significant time manually:

Screening candidate profiles
Understanding tech stacks
Generating relevant interview questions

This process is:

Time-consuming
Repetitive
Inconsistent across candidates

👉 Goal: Build a system that automates candidate evaluation and generates personalized technical questions.

🧠 Approach

Designed a modular AI system using Streamlit + LLMs:

Collected structured candidate inputs via UI
Used prompt engineering to generate 3–5 questions per technology
Enforced structured JSON responses for consistency
Implemented a fallback question engine for reliability
Stored candidate data locally for tracking and analysis
🔄 Iterations
V1: Static rule-based question generator
V2: Integrated LLM for dynamic generation
V3: Improved prompt design with structured outputs (JSON)
V4: Added fallback system for API failures
V5: Built full Streamlit UI with session-based interaction
⚙️ Key Design Choices
Streamlit → Rapid prototyping of interactive UI
LLM Prompting → Flexible and scalable question generation
Fallback System → Ensures 100% usability without API
CSV Storage → Lightweight persistence for demo
Modular Codebase → Clean separation of UI, logic, and prompts
💡 Features
Candidate data collection form
Tailored technical question generation
Multi-technology support
Chat-based interaction
Exit keyword handling
Local data persistence
Privacy-aware design
🧪 Tech Stack
Python
Streamlit
OpenAI API (LLMs)
Pandas, NumPy
Prompt Engineering
📊 Sample Output

👉 Example:
Input Tech Stack: Python, SQL

Generated Questions:

Explain Python decorators with an example
What are joins in SQL? Types?
Difference between list and tuple
How would you optimize a slow SQL query?
📸 Demo

👉 (Add screenshots here — VERY IMPORTANT)

Candidate form UI
Generated questions
Chat interface
🧱 Project Structure
talentscout-chatbot/
│── app.py
│── chatbot.py
│── prompts.py
│── utils.py
│── requirements.txt
│── data/
🔐 Data Privacy
Stores candidate data locally (CSV)
No sensitive data required
Designed with privacy-first approach
🚀 Future Improvements
Implement RAG (Retrieval-Augmented Generation)
Resume parsing using NLP
Candidate embeddings + vector database
Recruiter dashboard with analytics
Deployment with scalable backend

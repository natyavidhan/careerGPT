# CareerGPT

🚀 **CareerGPT** is an AI-powered career planning assistant that helps students explore career paths, identify skill gaps, generate personalized roadmaps, and even match with internships or jobs — all in one place.

---

## ✨ Features

### 1. **Career Suggestions + Confidence**

* Input: user interests & skills.
* Output: Top 3 career paths with confidence scores (⭐ ratings).
* Shows reasoning for transparency.

### 2. **Career Roadmap Generator**

* Auto-generates a **step-by-step timeline** (short-term, mid-term, long-term, expert-level).
* Includes: skills to learn, projects to build, certifications to pursue.
* Actionable milestones → not vague advice.

### 3. **Skill Gap Analysis**

* Compares user’s current skills vs. target career requirements.
* Outputs missing skills as a **checklist** for tracking progress.
* Prioritized (what to learn first, next, later).

### 4. **Internship/Job Matching (Live API)**

* Integrates with **Hiring.cafe API** to fetch real-time jobs.
* Cross-matches job descriptions with user skills.
* Returns top 3 matches with **fit scores** (%).
* Fallback: mock dataset if API is unavailable.

### 5. **Mini Progress Tracker**

* Saves last selected career/skills in session.
* When user returns → reminds them of unfinished steps.

---

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS) ──> Flask Backend ──> AI / Logic Layer
                                 │
                                 ├── Career Suggestions (LLM Prompt)
                                 ├── Roadmap Generator (LLM Prompt)
                                 ├── Skill Gap Analyzer (LLM Prompt)
                                 └── Internship/Job Matcher (Hiring.cafe API + local fallback)
```

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** Raw HTML, CSS, JavaScript (Jinja2 templating)
* **AI Layer:** Prompt-engineered LLM (for suggestions, roadmap, gaps)
* **Job Data:** Hiring.cafe API + JSON fallback
* **Storage:** Session variables + JSON files

---

## ⚙️ Installation & Setup

1. **Clone the repo**

```bash
git clone https://github.com/natyavidhan/careerGPT.git
cd careerGPT
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run Flask app**

```bash
python app.py
```

5. Open in browser → `http://127.0.0.1:5000`

---

## 📊 Example Flow

1. User enters interests → gets **career suggestions**.
2. Chooses a career → gets **personalized roadmap**.
3. Enters known skills → gets **gap analysis checklist**.
4. Fetches **internships/jobs live** → displays as cards.
5. Progress can be **saved and resumed later**.

---

## 📸 Working Demo
[Live Demo](https://careergpt-dhoomketu.vercel.app/)
[Video Demo](https://www.youtube.com/watch?v=e9MEkWejH2k)

---

## 🚀 Scalability & Future Scope

* Add **Gamification**: streaks, progress levels, badges.
* Add **Analytics Dashboard**: skill growth tracking, career readiness % over time.
* Multi-career exploration (compare Data Scientist vs. ML Engineer side by side).
* More live data sources: LinkedIn, Internshala, AngelList.
* Extend to **Finance/Market/Support agents** as separate modules.

---

## 👨‍💻 Team

Built by **Dhoomketu** for Phantom Agents.

---

⚡ *CareerGPT proves that with smart prompts, a clean stack, and one solid idea — you can build something that feels like the future of career guidance.*

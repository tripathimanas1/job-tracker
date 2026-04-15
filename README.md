# Job Application Tracker Agent

Paste a job URL. Get a resume score, gap analysis, and a tailored cover letter — all logged to CSV.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your Gemini API key to .env
```

Get your free Gemini API key at: https://aistudio.google.com

## Usage

**Analyze a job posting:**
```bash
python main.py analyze "https://jobs.example.com/ai-engineer"
```

**View all logged applications:**
```bash
python main.py history
```

**Skip cover letter generation:**
```bash
python main.py analyze "https://..." --no-cl
```

## What it does

1. Scrapes the job posting URL
2. Parses company, role, required skills
3. Scores your resume (1-10) with strengths and gaps
4. Drafts a tailored cover letter
5. Logs everything to `logs/applications.csv`
6. Saves cover letters to `logs/cover_letters/`

## Customize

- Edit `resume.txt` with your actual resume
- Tweak prompts in `analyzer.py` to match your voice

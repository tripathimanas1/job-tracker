import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"


def _call(prompt: str) -> str:
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()


def parse_jd(jd_text: str) -> dict:
    """Extract role, company, key skills, and requirements from raw JD text."""
    prompt = f"""
You are a job description parser.

Given this raw job posting text, extract the following in plain text (no markdown):
1. Company name
2. Role title
3. Top 5 required technical skills (comma separated)
4. Top 3 soft skills or traits they want
5. One sentence summary of what this role actually does day to day

Job posting:
{jd_text}

Respond in this exact format:
Company: <value>
Role: <value>
Tech Skills: <value>
Soft Skills: <value>
Summary: <value>
"""
    raw = _call(prompt)
    result = {}
    for line in raw.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def score_resume(jd_text: str, resume_text: str) -> dict:
    """Score how well the resume matches the JD."""
    prompt = f"""
You are a strict technical recruiter.

Score this resume against the job description on a scale of 1-10.

Job Description:
{jd_text}

Resume:
{resume_text}

Respond in this exact format:
Score: <number out of 10>
Strengths: <2-3 bullet points of what matches well>
Gaps: <2-3 bullet points of what is missing or weak>
Verdict: <one sentence on whether to apply>
"""
    raw = _call(prompt)
    result = {}
    for line in raw.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def draft_cover_letter(jd_text: str, resume_text: str, parsed_jd: dict) -> str:
    """Draft a tailored cover letter."""
    prompt = f"""
You are helping an AI/ML engineer write a cover letter.

Write a short, punchy cover letter (max 200 words) for this role.
- Lead with the problem the company is solving, not with "I am applying for..."
- Highlight 2 specific projects from the resume that are most relevant
- End with a clear call to action
- No fluff, no clichés, no "I am a passionate..."
- Tone: confident, direct, slightly entrepreneurial

Role: {parsed_jd.get('Role', 'this role')} at {parsed_jd.get('Company', 'your company')}

Job Description:
{jd_text}

Resume:
{resume_text}

Cover letter:
"""
    return _call(prompt)

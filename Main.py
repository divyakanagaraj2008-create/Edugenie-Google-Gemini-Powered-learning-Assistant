import os
import json
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from google import genai

# ============================================================
# EDUGENIE: GOOGLE GEMINI POWERED LEARNING ASSISTANT
# ============================================================

# ------------------------------------------------------------
# 1. GEMINI API KEY
# ------------------------------------------------------------
# OPTION 1:
# Set your API key as an environment variable:
#
# Windows CMD:
# set GEMINI_API_KEY=YOUR_API_KEY
#
# Windows PowerShell:
# $env:GEMINI_API_KEY="YOUR_API_KEY"
#
# OPTION 2:
# Put your API key directly below.
# Replace YOUR_API_KEY with your actual Gemini API key.
# ------------------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY")

client = genai.Client(api_key=API_KEY)

# Gemini model
MODEL_NAME = "gemini-2.5-flash"

# FastAPI application
app = FastAPI(title="EduGenie")


# ============================================================
# GEMINI FUNCTION
# ============================================================

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the response."""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"


# ============================================================
# 1. QUESTION & ANSWER MODULE
# ============================================================

def question_answer(question: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and clearly.

Question:
{question}

Instructions:
- Give a direct answer.
- Use simple language.
- Explain difficult terms if necessary.
- Keep the answer suitable for a student.
"""

    return ask_gemini(prompt)


# ============================================================
# 2. EXPLANATION MODULE
# ============================================================

def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI tutor.

Explain the following topic in a simple way so that a beginner
can easily understand it.

Topic:
{topic}

Give:
1. Simple definition
2. Main points
3. Example
4. Short summary

Avoid unnecessarily complicated language.
"""

    return ask_gemini(prompt)


# ============================================================
# 3. QUIZ MODULE
# ============================================================

def generate_quiz(topic: str) -> str:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions about:

{topic}

Each question must contain:
- question
- 4 options
- correct_answer
- explanation

Return ONLY valid JSON in this format:

[
    {{
        "question": "Question 1",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_answer": "A",
        "explanation": "Explanation"
    }},
    {{
        "question": "Question 2",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_answer": "B",
        "explanation": "Explanation"
    }},
    {{
        "question": "Question 3",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "correct_answer": "C",
        "explanation": "Explanation"
    }}
]
"""

    result = ask_gemini(prompt)

    # Remove Markdown code fences if Gemini adds them
    result = result.replace("```json", "").replace("```", "").strip()

    try:
        quiz = json.loads(result)

        output = ""

        for i, question in enumerate(quiz, 1):

            output += f"<div class='quiz-question'>"
            output += f"<h3>Question {i}</h3>"
            output += f"<p><b>{question['question']}</b></p>"

            for option in question["options"]:
                output += f"<p>◉ {option}</p>"

            output += (
                f"<p class='answer'>"
                f"<b>Correct Answer:</b> "
                f"{question['correct_answer']}"
                f"</p>"
            )

            output += (
                f"<p><b>Explanation:</b> "
                f"{question['explanation']}</p>"
            )

            output += "</div>"

        return output

    except Exception:
        return (
            "<b>Quiz generated, but the response could not be "
            "formatted automatically.</b><br><br>"
            + result
        )


# ============================================================
# 4. SUMMARY MODULE
# ============================================================

def summarize_text(text: str) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational content.

Content:
{text}

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Use bullet points where useful.
- Make it suitable for quick revision.
"""

    return ask_gemini(prompt)


# ============================================================
# 5. LEARNING PATH MODULE
# ============================================================

def learning_path(topic: str) -> str:

    prompt = f"""
You are EduGenie, a personalized learning assistant.

Create a structured learning path for:

{topic}

Organize it from beginner level to advanced level.

Include:

1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Suggested timeline
5. Practice activities
6. Useful learning resources
7. Final project or assessment idea

Keep the plan practical and easy for a student to follow.
"""

    return ask_gemini(prompt)


# ============================================================
# HTML PAGE
# ============================================================

HTML_PAGE = """
<!DOCTYPE html>

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>EduGenie - Learning Assistant</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #222;
}

.header {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    padding: 30px;
    text-align: center;
}

.header h1 {
    margin: 0;
    font-size: 32px;
}

.header p {
    margin-top: 8px;
    font-size: 16px;
}

.container {
    width: 90%;
    max-width: 900px;
    margin: 30px auto;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
}

select,
textarea {
    width: 100%;
    padding: 13px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 15px;
}

textarea {
    min-height: 160px;
    resize: vertical;
}

button {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 8px;
    background: #4f46e5;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #3730a3;
}

.result {
    margin-top: 25px;
    padding: 20px;
    background: #f8fafc;
    border-left: 5px solid #4f46e5;
    border-radius: 8px;
    line-height: 1.6;
    white-space: pre-wrap;
}

.quiz-question {
    background: white;
    padding: 18px;
    margin-bottom: 18px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

.answer {
    background: #ecfdf5;
    padding: 10px;
    border-radius: 6px;
}

.footer {
    text-align: center;
    margin: 30px;
    color: #777;
}

</style>

</head>

<body>

<div class="header">

<h1>🎓 EduGenie</h1>

<p>Google Gemini Powered Learning Assistant</p>

</div>


<div class="container">

<div class="card">

<form method="post" action="/process">

<label>Select Learning Task</label>

<select name="task">

<option value="qa">Question & Answer</option>

<option value="explain">Explain a Topic</option>

<option value="quiz">Generate Quiz</option>

<option value="summarize">Summarize Text</option>

<option value="learn">Learning Path</option>

</select>


<label>Enter your question, topic or text</label>

<textarea
name="user_input"
placeholder="Example: Explain Artificial Intelligence in simple words..."
required></textarea>


<button type="submit">
Generate Answer
</button>

</form>


{result}

</div>

</div>


<div class="footer">

EduGenie • Powered by Google Gemini

</div>

</body>

</html>
"""


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():

    page = HTML_PAGE.replace(
        "{result}",
        ""
    )

    return page


# ============================================================
# PROCESS USER REQUEST
# ============================================================

@app.post("/process", response_class=HTMLResponse)
async def process(
    task: str = Form(...),
    user_input: str = Form(...)
):

    if not user_input.strip():

        result = "<p>Please enter something first.</p>"

    elif task == "qa":

        result = question_answer(user_input)

    elif task == "explain":

        result = explain_topic(user_input)

    elif task == "quiz":

        result = generate_quiz(user_input)

    elif task == "summarize":

        result = summarize_text(user_input)

    elif task == "learn":

        result = learning_path(user_input)

    else:

        result = "Invalid task selected."

    page = HTML_PAGE.replace(
        "{result}",
        f"<div class='result'><h2>EduGenie Result</h2>{result}</div>"
    )

    return page


# ============================================================
# API ENDPOINTS
# ============================================================

@app.post("/qa")
async def qa_api(question: str = Form(...)):

    return {
        "answer": question_answer(question)
    }


@app.post("/explain")
async def explain_api(topic: str = Form(...)):

    return {
        "explanation": explain_topic(topic)
    }


@app.post("/quiz")
async def quiz_api(topic: str = Form(...)):

    return {
        "quiz": generate_quiz(topic)
    }


@app.post("/summarize")
async def summarize_api(text: str = Form(...)):

    return {
        "summary": summarize_text(text)
    }


@app.post("/learn/recommendations")
async def learning_api(topic: str = Form(...)):

    return {
        "learning_path": learning_path(topic)
    }


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
          )

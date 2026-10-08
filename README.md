# Science Tutor Chatbot

A small Flask web app that answers science questions (physics, chemistry, biology, astronomy, earth science) in plain
language, using Google Gemini. It stays in its domain: off-topic questions get a polite refusal instead of an answer.

## Features

- Chat UI (single page, mobile friendly) talking to a JSON API
- Domain guardrail in the system prompt: science only, plain-text answers
- `/health` endpoint for uptime checks
- API key read from the environment, never from code

## API

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/chat` | `{"message": "Why is the sky blue?"}` | `{"reply": "..."}` (400 if `message` is empty) |
| `GET` | `/health` | - | `{"status": "ok"}` |

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your-key" > .env               # get a key at aistudio.google.com/apikey
python app.py                                       # http://localhost:5000
```

`.env` is git-ignored - never commit it.

## Stack

Python, Flask, Google Gemini (`google-generativeai`), HTML/CSS/JavaScript.

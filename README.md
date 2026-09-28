# AI Study Buddy 🤖📚

A terminal chatbot powered by a Large Language Model (Claude by Anthropic) that helps students learn. It can tutor you, quiz you, or explain topics super simply.

## Features
- **3 learning modes** built with prompt engineering (Tutor, Quiz Master, Explain Like I'm 5)
- **Conversation memory** so the AI remembers what you said earlier
- **Streaming responses** that appear word-by-word
- **Chat saving** to JSON files
- **Secure API key handling** with a `.env` file

## Tech Stack
Python, Anthropic Claude API, python-dotenv

## How to Run
1. Install Python 3.9+
2. Install packages:
   ```
   pip install -r requirements.txt
   ```
3. Get an API key from https://console.anthropic.com
4. Copy `.env.example` to `.env` and paste your key in it
5. Run:
   ```
   python study_buddy.py
   ```

## Example
```
You: What is photosynthesis?
Buddy: Photosynthesis is how plants make their own food using sunlight...
```

## What I Learned
- How to call an LLM through an API
- How system prompts change an AI's behavior
- How chatbot memory works (sending conversation history)
- Keeping secrets like API keys out of code

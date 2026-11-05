# FAQ Chatbot

A Python-based FAQ assistant for ecommerce support queries. This project uses a lightweight NLP pipeline to match user questions against a predefined set of FAQs and return the most relevant answer.

## Overview

The app includes:
- A Streamlit web interface for chatting with the FAQ bot
- FAQ data stored in `faqs.json`
- Text preprocessing with NLTK
- TF-IDF vectorization and cosine similarity matching
- A simple, fast answer retrieval system for common customer support questions

## Project files

- `app.py` – Streamlit chat UI
- `chatbot.py` – FAQ matching logic and preprocessing
- `faqs.json` – Stored questions and answers used for retrieval

## Features

- Responds to common shopping and order-related questions
- Matches user input using semantic similarity, not exact string matching
- Includes fallback response when no relevant FAQ is found
- Easy to extend by adding more questions to `faqs.json`

## Requirements

Install the required dependencies:

```bash
pip install streamlit nltk scikit-learn
```

The first run will automatically download the NLTK datasets required for stopword removal and lemmatization.

## Run the app

Start the chatbot UI:

```bash
streamlit run app.py
```

You can also run the terminal version directly:

```bash
python chatbot.py
```

## Example FAQs covered

The bot supports questions related to:
- Order tracking
- Returns and refunds
- Shipping duration and cost
- Payment methods
- Account and password issues
- International delivery and contact support

## Customization

To add more support answers, edit `faqs.json` and add entries in this format:

```json
{
  "question": "How do I track my order?",
  "answer": "Go to 'My Orders' in your account and click 'Track'."
}
```

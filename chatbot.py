"""FAQ chatbot: NLTK preprocessing + TF-IDF + cosine similarity."""
import json
import re
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _ensure_nltk():
    for pkg, path in [("stopwords", "corpora/stopwords"), ("wordnet", "corpora/wordnet")]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)


_ensure_nltk()
_tokenizer = RegexpTokenizer(r"[a-z0-9]+")
_lemmatizer = WordNetLemmatizer()
try:
    _stop = set(stopwords.words("english")) - {"not", "no"}
except LookupError:  # offline fallback
    _stop = {"a", "an", "the", "is", "are", "do", "does", "i", "my", "me", "you",
             "your", "to", "of", "and", "or", "can", "how", "what", "when", "for", "in", "it"}


def preprocess(text: str) -> str:
    """Lowercase -> strip punctuation/tokenize -> remove stopwords -> lemmatize."""
    text = re.sub(r"\s+", " ", text.lower())
    tokens = _tokenizer.tokenize(text)
    out = []
    for t in tokens:
        if t in _stop:
            continue
        try:
            out.append(_lemmatizer.lemmatize(t))
        except LookupError:
            out.append(t)
    return " ".join(out)


class FAQBot:
    def __init__(self, faq_path="faqs.json", threshold=0.25):
        path = Path(__file__).parent / faq_path
        self.faqs = json.loads(path.read_text(encoding="utf-8"))
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(
            [preprocess(f["question"]) for f in self.faqs]
        )

    def ask(self, user_question: str):
        """Return (answer, matched_question, score)."""
        cleaned = preprocess(user_question)
        if not cleaned:
            return "Could you rephrase that?", None, 0.0
        scores = cosine_similarity(self.vectorizer.transform([cleaned]), self.matrix)[0]
        best = int(scores.argmax())
        if scores[best] < self.threshold:
            return ("Sorry, I couldn't find a good answer. Try rephrasing, "
                    "or contact support@example.com."), None, float(scores[best])
        return self.faqs[best]["answer"], self.faqs[best]["question"], float(scores[best])


if __name__ == "__main__":
    bot = FAQBot()
    print("FAQ Bot (type 'quit' to exit)")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        answer, matched, score = bot.ask(q)
        print(f"Bot: {answer}" + (f"\n     [matched: '{matched}' | score {score:.2f}]" if matched else ""))
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LocalRetriever:
    def __init__(self, directory: Path, top_k: int = 3, min_score: float = 0.05):
        self.directory = directory
        self.top_k = top_k
        self.min_score = min_score
        self.names: list[str] = []
        self.documents: list[str] = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None
        self._load()

    def _load(self) -> None:
        for path in sorted(self.directory.glob("*.txt")):
            self.names.append(path.name)
            self.documents.append(path.read_text(encoding="utf-8"))
        if self.documents:
            self.matrix = self.vectorizer.fit_transform(self.documents)

    def search(self, query: str) -> list[dict]:
        if not self.documents:
            return []
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        indices = np.argsort(scores)[::-1][: self.top_k]
        results = []
        for index in indices:
            score = float(scores[index])
            if score >= self.min_score:
                results.append({
                    "source": self.names[index],
                    "score": round(score, 4),
                    "content": self.documents[index],
                })
        return results

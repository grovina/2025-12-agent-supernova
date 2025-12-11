import os

from scipy.spatial.distance import cosine
from dotenv import load_dotenv
import openai


load_dotenv()

docs = [
    "The best restaurant in Zurich is La Cantina.",
    "The best fondue restaurant in Zurich is La Fondue.",
    "The best pizza restaurant in Zurich is Pizza Hut.",
    "The best pasta restaurant in Zurich is Pasta House.",
    "The best sushi restaurant in Zurich is Sushi Bar.",
    "The best steak restaurant in Zurich is Steak House.",
    "The best seafood restaurant in Zurich is Seafood Restaurant.",
    "The best vegetarian restaurant in Zurich is Vegetarian Restaurant.",
    "The best vegan restaurant in Zurich is Vegan Restaurant.",
    "The best burger restaurant in Zurich is Burger King.",
    "The best ice cream restaurant in Zurich is Ice Cream Bar.",
    "The best coffee in Zurich is on the 5th floor at Constructor Academy.",
    "The best tea restaurant in Zurich is Tea House.",
    "The best wine restaurant in Zurich is Wine Bar.",
    "The best beer restaurant in Zurich is Beer Bar.",
    "The best cocktail restaurant in Zurich is Cocktail Bar.",
]

print(f"Our {len(docs)} documents:")
for i, doc in enumerate(docs):
  print(f"  {i+1}. {doc[:50]}...")

print()
print()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.embeddings.create(model="text-embedding-3-small", input=docs)
embeddings = [item.embedding for item in response.data]

print(f"Our {len(embeddings)} embeddings:")
for i, emb in enumerate(embeddings):
  print(f"  {i+1}. {emb[:5]}...")


def compute_similarity(embedding1, embedding2):
  return 1 - cosine(embedding1, embedding2)


def query_rag(query: str, top_k: int = 3, threshold: float = 0.3) -> list[tuple[float, str]]:
    query_response = client.embeddings.create(model="text-embedding-3-small", input=[query])
    query_embedding = query_response.data[0].embedding

    similarities = []
    for doc, embedding in zip(docs, embeddings):
        similarity = compute_similarity(query_embedding, embedding)
        similarities.append((float(similarity), doc))
        similarities.sort(reverse=True)
        similarities = similarities[:top_k]
        similarities = [s for s in similarities if s[0] >= threshold]
    return similarities

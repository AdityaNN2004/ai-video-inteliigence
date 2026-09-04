from app.services.embedding import generate_embedding


text = "Thanks to more effective communication."

embedding = generate_embedding(text)

print("Embedding dimensions:", len(embedding))
print("First 5 values:", embedding[:5])
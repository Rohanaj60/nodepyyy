import sys
import json
from sentence_transformers import SentenceTransformer

# Load the pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to generate embeddings
def generate_embeddings(sentences):
    embeddings = model.encode(sentences)
    return embeddings.tolist()  # Convert embeddings to list for JSON serialization

if __name__ == "__main__":
    input_data = sys.stdin.read()  # Read input from stdin
    queries = json.loads(input_data)
    embeddings = generate_embeddings(queries)
    print(json.dumps(embeddings))  # Output embeddings as JSON

import sys

import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import numpy as np

# Load the pretrained model
model = SentenceTransformer("all-mpnet-base-v2")

# Get the input sentence (query) from the command line argument
sentence = sys.argv[1]  # Query is passed as the first argument

# Generate embedding for the sentence
# sentence_embedding = model.encode([sentence])


# 2. Use NLTK's sentence tokenizer for better segmentation
story_sentences = sent_tokenize(sentence)

# Optional: Remove any very short sentences or empty sentences
story_sentences = [sentence.strip() for sentence in story_sentences if len(sentence.strip()) > 5]
# story_sentences = [sentence.strip() for sentence in story_sentences if sentence.strip()]


# 3. Generate embeddings for the sentences in the story
sentence_embeddings = model.encode(story_sentences)

# Print the embedding (this will be captured by Node.js)
print(sentence_embeddings.tolist())  # Convert to list for JSON serialization

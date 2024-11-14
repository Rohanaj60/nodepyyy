import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from scipy.spatial.distance import euclidean
import numpy as np
# Download the punkt resource needed for sentence tokenization
nltk.download('punkt')

# 1. Load the pretrained model
# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("all-mpnet-base-v2")


# Story text to encode
story = """ 
Rohan is a skilled software developer with experience in multiple technologies. He has worked on projects involving web applications, mobile APIs, and AI chatbots. 
Rohan is passionate about developing scalable, efficient applications and is always learning new tools and frameworks to stay up to date with the latest trends in the industry.
On weekends, Rohan loves to explore new coding languages and frameworks. He has recently started experimenting with machine learning algorithms. His passion for technology keeps him constantly motivated. Rohan is 24 Years old.
"""

# 2. Use NLTK's sentence tokenizer for better segmentation
story_sentences = sent_tokenize(story)

# Optional: Remove any very short sentences or empty sentences
story_sentences = [sentence.strip() for sentence in story_sentences if len(sentence.strip()) > 5]
# story_sentences = [sentence.strip() for sentence in story_sentences if sentence.strip()]


# 3. Generate embeddings for the sentences in the story
sentence_embeddings = model.encode(story_sentences)

# 4. Define the query
# query = "What does Rohan love to do on weekends?"

query = "what is he currently working on?"

# 5. Generate embedding for the query
query_embedding = model.encode([query])

# 6. Calculate cosine similarities between the query and each sentence embedding
# cosine_similarities = cosine_similarity(query_embedding, sentence_embeddings)
cosine_similarities = cosine_similarity(query_embedding, sentence_embeddings)

# 7. Get the index of the most similar sentence
# most_similar_idx = similarities.argmax()

# # 8. Retrieve the most relevant sentence
# most_similar_sentence = story_sentences[most_similar_idx]
# print(f"Query: {query}")
# print(f"Most relevant sentence: {most_similar_sentence}")
euclidean_distances = [euclidean(query_embedding[0], sentence_embedding) for sentence_embedding in sentence_embeddings]

# 8. Combine both cosine similarity and Euclidean distance to rank results
# Normalize Euclidean distances to be between 0 and 1
max_distance = max(euclidean_distances)
normalized_euclidean = [distance / max_distance for distance in euclidean_distances]

# The final score can be a combination of cosine similarity and Euclidean distance
final_scores = [(cosine_similarities[0][i], normalized_euclidean[i]) for i in range(len(cosine_similarities[0]))]

# 9. Sort sentences based on a weighted combination of cosine similarity and Euclidean distance
# You can adjust the weights for cosine and Euclidean as needed
weights = (0.7, 0.3)  # Adjust this to give more weight to either cosine similarity or Euclidean distance
sorted_sentences = sorted(zip(story_sentences, final_scores), key=lambda x: (weights[0] * x[1][0] - weights[1] * x[1][1]), reverse=True)

# 10. Output the most relevant sentence
print(f"Query: {query}")
print(f"Most relevant sentence: {sorted_sentences[0][0]}")
# # 7. Sort sentences based on similarity
# most_similar_idx = cosine_similarities.argmax()

# # 8. Retrieve the most relevant sentence
# most_similar_sentence = story_sentences[most_similar_idx]
# print(f"Query: {query}")
# print(f"Most relevant sentence: {most_similar_sentence}")

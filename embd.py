# from sentence_transformers import SentenceTransformer

# # 1. Load a pretrained Sentence Transformer model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # The sentences to encode
# sentences = [
#     "The weather is lovely today.",
#     "It's so sunny outside!",
#     "He drove to the stadium.",
# ]

# # 2. Calculate embeddings by calling model.encode()
# embeddings = model.encode(sentences)
# print(embeddings.shape)
# # [3, 384]

# # 3. Calculate the embedding similarities
# # similarities = model.similarity(embeddings, embeddings)
# # print(similarities)
# # tensor([[1.0000, 0.6660, 0.1046],
# #         [0.6660, 1.0000, 0.1411],
# #         [0.1046, 0.1411, 1.0000]])



import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import numpy as np

nltk.download('punkt')
from nltk.tokenize import sent_tokenize


# 1. Load the pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")
# model = SentenceTransformer("all-mpnet-base-v2")

# model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")


# The story paragraph to encode (split into sentences for semantic search)
# story = """
# On a bright Sunday morning, Emily decided to go for a walk in the park. She loved the crisp air and the golden autumn leaves scattered on the ground. 
# As she strolled, she saw children playing, couples enjoying picnics, and dogs running freely. After a while, she found a cozy spot under a large oak tree 
# where she sat and read her favorite book. It was a peaceful day, and Emily felt content just being surrounded by nature's beauty.
# """


story = """
Rohan Joshi is a software developer with experience in both frontend and backend technologies. He is proficient in using tools like Laravel, Vue.js, React.js, Node.js, and MongoDB. Rohan has worked on several projects, including web applications and mobile APIs. He is passionate about learning new technologies and building scalable applications. In addition to his work on development, Rohan is also exploring the world of AI and chatbot development, aiming to create intelligent systems that can interact with users seamlessly. He is focused on enhancing his skills to build efficient, modern applications while maintaining a keen interest in optimizing workflows for productivity.

"""

# 2. Split the story into sentences
# story_sentences = story.split('.')
story_sentences = sent_tokenize(story)


# Remove any empty sentences or extra spaces
story_sentences = [sentence.strip() for sentence in story_sentences if sentence.strip()]

# 3. Generate embeddings for the sentences in the story
sentence_embeddings = model.encode(story_sentences)

# 4. Query (question) to ask the story
# query = "Where did Emily sit?"
# query = "what is the girl name?"
# query = "What do she love ?"

query = "What is Rohan exploring now?"
# query = "What does Rohan use for backend development?"


# 5. Generate embedding for the query
query_embedding = model.encode([query])

# 6. Calculate cosine similarities between the query and each sentence embedding
similarities = cosine_similarity(query_embedding, sentence_embeddings)
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
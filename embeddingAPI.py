# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from sentence_transformers import SentenceTransformer
# from typing import List

# # Load the pre-trained model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Initialize FastAPI app
# app = FastAPI()

# # Define request schema
# class EmbeddingRequest(BaseModel):
#     queries: List[str]

# # Define an endpoint for generating embeddings
# @app.post("/generate_embeddings")
# async def generate_embeddings(request: EmbeddingRequest):
#     sentences = request.queries
    
#     if not sentences:
#         raise HTTPException(status_code=400, detail="No queries provided")
    
#     embeddings = model.encode(sentences).tolist()
#     return {"embeddings": embeddings}

# # Run the app with: uvicorn embedding_api:app --reload


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List
import asyncio
from asyncio import Queue

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Define request schema
class EmbeddingRequest(BaseModel):
    queries: List[str]

# Create a queue for requests
request_queue = Queue(maxsize=100)  # Limit the queue size to control request load

async def process_embeddings(sentences):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, model.encode, sentences)

@app.post("/generate_embeddings")
async def generate_embeddings(request: EmbeddingRequest):
    sentences = request.queries
    if not sentences:
        raise HTTPException(status_code=400, detail="No queries provided")
    
    await request_queue.put(sentences)  # Add request to the queue
    embeddings = await process_embeddings(await request_queue.get())  # Process when it reaches the front of the queue
    request_queue.task_done()  # Mark as complete
    
    return {"embeddings": embeddings.tolist()}

# uvicorn embeddingAPI:app --workers 4 --host localhost --port 8000 --limit-concurrency 500 --timeout-keep-alive 5

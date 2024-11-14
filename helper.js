const axios = require('axios');

async function getEmbeddings(queries) {
  try {
    // Use 127.0.0.1 instead of localhost to avoid potential IPv6 issues
    const response = await axios.post('http://127.0.0.1:8000/generate_embeddings', { queries });
    return response.data.embeddings;
  } catch (error) {
    console.error("Error generating embeddings:", error.message);
    throw new Error("Embedding generation failed");
  }
}

module.exports = {getEmbeddings}
// Example usage:
// const queries = [
//   "What is the capital of France?",
//   "Tell me about machine learning.",
//   "How does embedding work?",
// ];

// getEmbeddings(queries)
//   .then(embeddings => {
//     console.log('Embeddings:', embeddings);
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });

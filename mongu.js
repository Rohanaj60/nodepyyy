// const { MongoClient } = require('mongodb');
const { getEmbeddings } = require('./helper'); // Assuming the helper function is in a separate file

// MongoDB URI
// const uri = 'mongodb+srv://rnzaj60:passwordcluster0.zjhsp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
// const client = new MongoClient(uri);

const { MongoClient, ServerApiVersion } = require('mongodb');
// const uri = "mongodb+srv://rnzaj60:root@cluster0.zjhsp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
const uri = "mongodb://rnzaj60:root@cluster0-shard-00-01.zjhsp.mongodb.net:27017/chatbot?ssl=true&replicaSet=atlas-bcsa84-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
// const client = new MongoClient(uri, {
//   serverApi: {
//     version: ServerApiVersion.v2,  // Use API version 2 or higher
//     // strict: true,
//     deprecationErrors: true,
//   }
// });
const client = new MongoClient(uri);


async function updateUserEmbeddings() {
  try {
    await client.connect();
    const database = client.db('chatbot');
    const usersCollection = database.collection('users');

    // Assuming you have an API or a method to generate embeddings
    // const generateEmbedding = async (text) => {
    //   // Replace this with your actual embedding generation logic
    //   const response = await axios.post('your-embedding-api-url', { text });
    //   return response.data.embedding; // Assuming the embedding is in `response.data.embedding`
    // };

    const users = await usersCollection.find({}).toArray();

    const updates = users.map(async (user,index) => {
      // const nameEmbedding = await getEmbeddings([user.name]);
      // const locationEmbedding = await getEmbeddings([user.location]);
      // const emailEmbedding = await getEmbeddings([user.email]);
      // Concatenate the fields
const combinedText = `${user.name} ${user.location} ${user.email}`;

// Generate a single embedding for the combined text
const combineEmbedding = await getEmbeddings([combinedText]);
      // const combineEmbedding = await getEmbeddings([user.name,user.location,user.email])
      // const nameEmbedding = 'test name embedding';
      // const locationEmbedding = 'test locaition embedding';
      // const emailEmbedding = 'test email embedding';


      await usersCollection.updateOne(
        { _id: user._id },
        {
          // $set: {
          //   "embeddings.name_embedding": nameEmbedding,
          //   "embeddings.location_embedding": locationEmbedding,
          //   "embeddings.email_embedding": emailEmbedding,

          // },
          $set: {
            "embeddings": combineEmbedding,
          },
        }
      );
    console.log(`${index} Embedding updated successfully!`);

    });

    await Promise.all(updates);
    console.log('Embeddings updated successfully!');
  } finally {
    await client.close();
  }
}

async function fetchSimilardedUsers(query) {
  try {
    await client.connect();
    const database = client.db('chatbot');
    const usersCollection = database.collection('users');
    const queryVector = await getEmbeddings([query]);
    // Vector Search pipeline for finding similar name embeddings
    const pipeline = [
      {
        // $match:{email:"test"}
        $vectorSearch: {
          index: "vector_index_users",  // Replace with the name of your index in Atlas
          queryVector: queryVector,
          path: "embeddings.name_embedding",
         numCandidates: 5,  // Specify the number of candidate documents to consider

       //   k: 5,  // Number of similar results to return
          similarity: "cosine",  // Can be "euclidean", "cosine", or "dotProduct"
        }
      },
      {
        $limit: 5  // Limit the results to 5 documents (or adjust based on your needs)
      }
     
    ];

    const results = await usersCollection.aggregate(pipeline).toArray();
    console.log("Similar Users:", results);
  } catch (error) {
    console.error("Error fetching similar users:", error);
  } finally {
    await client.close();
  }
}async function fetchSimilarUsers(query) {
  try {
    await client.connect();
    const database = client.db('chatbot');
    const usersCollection = database.collection('users');

    // Get the embedding for the query input
    // const queryVector = await getEmbeddings([query]);

    const queryVectorArray = await getEmbeddings([query]);  // Assuming this returns an array of vectors
    const queryVector = queryVectorArray[0]; 

    console.log({queryVector,queryVectorArray})
    // Vector Search pipeline for finding similar name embeddings
    const pipeline = [
      {
        $vectorSearch: {
          index: "vector_index_combined", // Replace with the name of your index in Atlas
          queryVector: queryVector,  // The query vector generated from the user input
          path: "embeddings",  // The field where the vector embeddings are stored
          numCandidates: 100,  // Number of candidates to consider (you can adjust this as needed)
          similarity: "cosine",  // Similarity type (cosine similarity)
      limit:5,

        },
      },
   
    ];
    const pipeline232323 = [
      {
        $search: {
          index: "vector_index_users",  // Your Atlas Search vector index name
          
                knnBeta: {
          path: ["embeddings.name_embedding","embeddings.location_embedding","embeddings.email_embedding"],  // The field where the vector embeddings are stored

                  // path: "embeddings.name_embedding", // The first vector field in your documents
                  vector: queryVector, // The vector representing your search query
                  k: 5 // Return top 5 closest matches for this field
                }
             
        }
      },
      {
        $limit: 10 // Limit the total number of results to 10 (can be adjusted as needed)
      }
    ];

    // const results = await usersCollection.aggregate(pipeline)

    const results = await usersCollection.aggregate(pipeline).toArray();

    console.log("Similar Users:", results);
  } catch (error) {
    console.error("Error fetching similar users:", error);
  } finally {
    await client.close();
  }
}
// uvicorn embeddingAPI:app --host localhost --port 8000 --reload


fetchSimilarUsers('give me all the users from the east joshep');


// fetchSimilarUsers('test');

// updateUserEmbeddings().catch(console.error);

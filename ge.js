const { spawn } = require('child_process');

// Function to run the Python script and get the embedding
function generateEmbedding(query) {
  return new Promise((resolve, reject) => {
    // Spawn the Python process to run the script
    const python = spawn('python', ['generate_embedding.py', query]);

    let output = '';

    // Collect the output from the Python script
    python.stdout.on('data', (data) => {
      output += data.toString();
    });

    // Handle errors from the Python script
    python.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    // Resolve the promise when the process ends
    python.on('close', (code) => {
      if (code === 0) {
        try {
          // Parse the output as JSON (the embedding will be a list)
          const embedding = JSON.parse(output);
          resolve(embedding);  // Return the embedding
        } catch (err) {
          reject(`Error parsing Python output: ${err}`);
        }
      } else {
        reject(`Python process exited with code ${code}`);
      }
    });
  });
}

// Example usage
const query = "What is Rohan's age?";
generateEmbedding(query)
  .then((embedding) => {
    console.log('Generated Embedding:', embedding);
  })
  .catch((error) => {
    console.error('Error:', error);
  });

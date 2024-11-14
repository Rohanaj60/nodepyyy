const { spawn } = require('child_process');
const path = require('path');

function getEmbeddings(queries) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [path.join(__dirname, 'embedding.py')]);

    // Send queries to Python script via stdin
    pythonProcess.stdin.write(JSON.stringify(queries));
    pythonProcess.stdin.end();

    // Capture output from Python
    pythonProcess.stdout.on('data', (data) => {
      try {
        const embeddings = JSON.parse(data.toString());
        resolve(embeddings);
      } catch (error) {
        reject("Error parsing Python response: " + error);
      }
    });

    // Handle errors
    pythonProcess.stderr.on('data', (data) => {
      console.error('stderr: ' + data.toString());
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(`Python process exited with code ${code}`);
      }
    });
  });
}

// // Example queries to send
// const queries = [
//   "What is the capital of France?",
//   "Tell me about machine learning.",
//   "How does embedding work?",
// ];

// Get embeddings for the queries
getEmbeddings(queries)
  .then(embeddings => {
    console.log('Embeddings:', embeddings);
  })
  .catch(error => {
    console.error('Error:', error);
  });

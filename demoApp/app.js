const express = require('express');
const app = express();
const port = process.env.PORT || 8080; // Use environment variable for port

app.get('/', (req, res) => {
    res.send('Hello from Node.js!');
});

app.listen(port, () => {
    console.log(`Node.js app listening at http://localhost:${port}`);
});
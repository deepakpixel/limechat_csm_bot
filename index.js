require('dotenv').config();
const express = require('express');
const app = express();
app.get('create-order', (req, res) => {
  console.log('BODY: ', req.body);
  if (req.headers['Authorization'] !== process.env.AUTH_SECRET) return;
});
PORT = process.env.PORT;
app.listen(PORT, () =>
  console.log(`Server is up and running 🚀 on port ${{ PORT }}`)
);

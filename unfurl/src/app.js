const express = require('express');
const path = require('path');

const publicRoutes = require('./routes/publicRoutes');

const app = express();

app.use(express.static('public'));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.use('/', publicRoutes);

const PORT = 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`[INFO] Public app running on http://0.0.0.0:${PORT}`);
});

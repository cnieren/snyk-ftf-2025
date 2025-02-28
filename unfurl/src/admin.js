const express = require('express');
const morgan = require('morgan');
const adminRoutes = require('./routes/adminRoutes');

const adminApp = express();
adminApp.use(express.urlencoded({ extended: true }));
adminApp.use(express.json());
adminApp.use(morgan('combined'));

adminApp.use('/', adminRoutes);

// This should keep people away from the admin panel!
function getRandomPort() {
    const MIN_PORT = 1024;
    const MAX_PORT = 4999;
    let port;
    do {
        port = Math.floor(Math.random() * (MAX_PORT - MIN_PORT + 1)) + MIN_PORT;
    } while (port === 5000);
    return port;
}

const adminPort = getRandomPort();
adminApp.listen(adminPort, '127.0.0.1', () => {
    console.log(`[INFO] Admin app running on http://127.0.0.1:${adminPort}`);
});

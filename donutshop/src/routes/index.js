const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.render('index', {
        title: 'D0nutShop - The Best Donuts in Town'
    });
});

router.get('/admin', (req, res) => {
    res.render('admin');
});

module.exports = router;

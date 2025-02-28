const express = require('express');
const { unfurlUrl } = require('./helpers');
const axios = require('axios');
const cheerio = require('cheerio');
const router = express.Router();

router.post('/unfurl', async (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.status(400).json({ error: 'No URL provided!' });
    }

    try {
        const response = await axios.get(url);
        const html = response.data;
        const $ = cheerio.load(html);

        const title = $('title').text() || 'No title found';
        const description = $('meta[name="description"]').attr('content') || 'No description found';

        let image = $('meta[property="og:image"]').attr('content') || $('link[rel="icon"]').attr('href') || '';
        if (image && !image.startsWith('http')) {
            const urlObj = new URL(url);
            image = `${urlObj.origin}${image}`;
        }

        console.log(`[INFO] Unfurled metadata: Title: "${title}", Description: "${description}", Image: "${image}"`);

        res.json({ title, description, html, image });
    } catch (error) {
        console.error(`[ERROR] Failed to unfurl URL: ${error.message}`);
        res.status(404).json({ error: 'Failed to unfurl the URL.' });
    }
});

module.exports = router;

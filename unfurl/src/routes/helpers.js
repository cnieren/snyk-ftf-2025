const axios = require('axios');
const cheerio = require('cheerio');

async function unfurlUrl(url) {
    try {
        const response = await axios.get(url);
        const html = response.data;
        const $ = cheerio.load(html);

        const title = $('title').text() || 'No title found';
        const description = $('meta[name="description"]').attr('content') || 'No description found';

        console.log(`[INFO] Captured HTML from ${url}, length: ${html.length} characters`);

        return { title, description };
    } catch (error) {
        console.error(`[ERROR] Failed to unfurl URL: ${error.message}`);
        throw error;
    }
}

module.exports = { unfurlUrl };

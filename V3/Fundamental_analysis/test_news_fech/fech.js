const axios = require('axios');

async function getHTML(url) {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('An error occurred:', error.message);
    }
}

async function getPTags(html) {
    const pTagRegex = /<p[^>]*>([^<]+)<\/p>/gi;
    const matches = html.match(pTagRegex);
    if (matches) {
        return matches.map(match => match.replace(/<[^>]+>/g, ''));
    } else {
        return [];
    }
}

async function main() {
    const url = process.argv[2];
    const html = await getHTML(url);
    if (html) {
        const pTags = await getPTags(html);
        console.log(JSON.stringify(pTags)); // Print as JSON string
    }
}

main();

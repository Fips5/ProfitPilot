const axios = require('axios');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

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
    rl.question("Enter the URL: ", async (url) => {
        const html = await getHTML(url);
        if (html) {
            const pTags = await getPTags(html);
            console.log(pTags);
        }
        rl.close();
    });
}

main();

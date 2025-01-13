import axios from 'axios';
const getQuote = async () => {
    try {
        const response = await axios.get('/get_quote/');
        if (response.data.quote) {
            const quote = response.data.quote;
            const author = response.data.author;

            const quoteElement = document.getElementById('quote');
            const authorElement = document.getElementById('author');

            quoteElement.innerText = `"${quote}"`;
            authorElement.innerText = `- ${author}`;
        } else {
            console.error('Failed to fetch a quote:', response.data.error);
        }
    } catch (error) {
        console.error('Error fetching a quote:', error);
    }
};

getQuote();
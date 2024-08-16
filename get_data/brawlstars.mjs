import dotenv from 'dotenv';
dotenv.config();

import fetch from 'node-fetch';

const token = process.env.API_TOKEN;

fetch('https://api.brawlstars.com/v1/players/%238CCYQG9P', {
    headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
    }
}).then(response => response.json()).then(data => {
    console.log(data);
}).catch(err => {
    console.error(err);
});
import dotenv from 'dotenv';
import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();
const token = process.env.API_TOKEN;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const outputDir = path.join(__dirname, 'output');
const filePath = path.join(outputDir, 'rankings.json');

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

fetch('https://api.brawlstars.com/v1/rankings/global/players', {
    headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
    }
})
    .then(response => response.json())
    .then(data => {
        fs.writeFile(path.join(filePath), JSON.stringify(data, null, 2), (err) => {
            if (err) {
                console.error('Error writing to file', err);
            } else {
                console.log('JSON data saved successfully!');
            }
        });
    })
    .catch(err => {
        console.error('Error fetching data', err);
    });
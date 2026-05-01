import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

// ES6 module equivalents for __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;

// Enable CORS and JSON parsing
app.use(cors());
app.use(express.json());

// Main endpoint to play music
app.post('/api/play-music', async (req, res) => {
    const { query } = req.body;

    // Input validation: reject empty queries
    if (!query || query.trim() === '') {
        return res.status(400).json({ error: 'Query is required' });
    }

    try {
        // Resolve path to the Python automation script
        // Assumes backend/ and automation/ are sibling directories
        const scriptPath = path.resolve(__dirname, '../automation/automation.py');
        
        // Spawn the Python process
        const pythonProcess = spawn('python', [scriptPath, query]);

        let isResponseSent = false;

        // Listen for stdout from Python
        pythonProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            console.log(`Python Output: ${output}`);

            if (!isResponseSent) {
                if (output.includes('DECLINED')) {
                    isResponseSent = true;
                    return res.status(400).json({ error: 'Not a music request' });
                } else if (output.includes('VALIDATED:')) {
                    isResponseSent = true;
                    // The string looks like "VALIDATED: <keywords>"
                    const keywords = output.split('VALIDATED:')[1].trim();
                    return res.status(200).json({ 
                        message: 'Music request validated',
                        keywords: keywords
                    });
                }
            }
        });

        // Listen for stderr from Python
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data.toString()}`);
            // Note: Playwright sometimes outputs to stderr for non-fatal warnings
            // So we don't automatically fail the request here, but log it.
        });

        // Handle process exit
        pythonProcess.on('close', (code) => {
            console.log(`Python process exited with code ${code}`);
            if (!isResponseSent && code !== 0) {
                return res.status(500).json({ error: 'Automation process failed' });
            }
        });

    } catch (error) {
        console.error('Server error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

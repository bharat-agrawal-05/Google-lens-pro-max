const express = require('express');
const dotenv = require('dotenv').config();
const cors = require('cors');
const multer = require('multer');
const {spawn} = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 5000;
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, './uploads')
    },
    filename: function (req, file, cb) {
      cb(null, 'input-file.png')
    }
  })
  
const upload = multer({ storage: storage });

app.post('/upload', upload.single('file'), (req, res) => {
    const prompt = req.body.prompt;
    const imgPath = path.join(__dirname, 'uploads', 'input-file.png');
    const pythonProcess = spawn('python3', ['script.py', imgPath, prompt]);
    pythonProcess.on('close', (code) => {
        if (code === 0) {
          const csvFilePath = path.join(__dirname, 'output.csv'); 
    
          if (fs.existsSync(csvFilePath)) {
            res.setHeader('Content-Disposition', 'attachment; filename="output.csv"');
            res.setHeader('Content-Type', 'text/csv');
            res.sendFile(csvFilePath, (err) => {
              if (err) {
                console.error('Error sending file:', err);
                res.status(500).send('Error sending the file');
              } else {
                console.log('CSV file sent successfully');
              }
            });
          } 
          else {
            res.status(500).json({ error: 'CSV file not found' });
          }
        } 
        else {
          res.status(500).json({ error: 'Python script failed to generate CSV' });
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
        res.status(500).send('Error running Python script');
    });
})

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
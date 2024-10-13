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

let responseSent = false;
let fileExt = '';
let fileName = '';
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, './uploads')
    },
    filename: function (req, file, cb) {
      fileExt = file.originalname.split('.').pop();
      fileName = 'input-file' + '.' + fileExt;
      cb(null, fileName)
    }
  })
  
const upload = multer({ storage: storage });

app.post('/upload', upload.single('file'), (req, res) => {
    const prompt = req.body.prompt;
    const imgPath = path.join(__dirname, 'uploads', fileName);
    const pythonProcess = spawn('python3', ['app.py', imgPath, prompt]);
    pythonProcess.on('close', (code) => {
        if (code === 0) {
          const csvFilePath = path.join(__dirname, 'output.csv');
    
          if (fs.existsSync(csvFilePath)) {
            res.setHeader('Content-Disposition', 'attachment; filename="output.csv"');
            res.setHeader('Content-Type', 'text/csv'); 
            res.sendFile(csvFilePath, (err) => {
              if (err) {
                if (!responseSent) {
                  responseSent = true;
                  return res.status(500).send('Error sending the file');
                }
              } 
              console.log('CSV file sent successfully');
            });
          } 
          else {
            if (!responseSent) {
              responseSent = true;
              res.status(500).json({ error: 'CSV file not found' });
            }
          }
        } 
        else {
          if (!responseSent) {
            responseSent = true;
            console.log('FUCK THIS SHIT') 
            res.status(500).json({ error: 'Python script failed to generate CSV' });
          }
        }
    });
});

app.get('/caption', (req, res) => {
  const filePath = path.join(__dirname, 'caption.txt');
    res.sendFile(filePath, (err) => {
        if (err) {
          console.error('Error sending file:', err);
          res.status(err.status).end();
        }
        console.log('Caption File sent successfully')
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
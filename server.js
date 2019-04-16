var express = require('express');

var morgan = require('morgan')
var path = require('path')
var rfs = require('rotating-file-stream')

var app = express()

// create a rotating write stream
var accessLogStream = rfs('access.log', {
  interval: '1d', // rotate daily
  path: path.join(__dirname, 'public/log')
})

// setup the logger
app.use(morgan('combined', { stream: accessLogStream }))
var multer  = require('multer');
const { spawn } = require('child_process');


const imageFilter = function (req, file, cb) {
    // accept image only
    if (!file.originalname.match(/\.(jpg|jpeg|png|gif)$/)) {
        return cb(new Error('Only image files are allowed!'), false);
    }
    cb(null, true);
};
var storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, 'uploads/')
    },
    filename: (req, file, cb) => {
      cb(null, file.originalname)
    }
});

var upload = multer({ storage });

var options = {
  dotfiles: 'ignore',
  etag: false,
  extensions: ['htm', 'html'],
  maxAge: '1d',
  redirect: false,
  setHeaders: function (res, path, stat) {
    res.set('x-timestamp', Date.now())
  }
}

app.use(express.static('public', options));

app.post('/', upload.single('kek'), function (req, res, next) {
	const imgpython = spawn('python3', ['main.py', './uploads/' + req.file.originalname]);

	imgpython.stdout.on('data', (data) => {
	  console.log(`stdout: ${data}`);
	});

	imgpython.stderr.on('data', (data) => {
	  console.log(`stderr: ${data}`);
	});

	imgpython.on('close', (code) => {
	  res.send(`child process exited with code ${code}`);
	});
});

app.listen(80, function () {
  console.log('Example app listening on port 3000!');
});
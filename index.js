const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'mod1',
  password: 'vladik08102002',
  port: 5432,
});

const jsonParser = bodyParser.json();

app.get('/list', (req, res) => {
  pool.query('SELECT * FROM students', (err, result) => {
    if (err) {
      res.status(500).send(err.message);
    } else {
      res.json(result.rows);
    }
  });
});

app.post('/auth', jsonParser, (req, res) => {
  const nickname = req.body.nickname;
  pool.query('SELECT * FROM students WHERE nickname = $1', [nickname], (err, result) => {
    if (err) {
      res.status(500).send(err.message);
    } else if (result.rows.length === 0) {
      res.status(404).send('Not found');
    } else {
      const token = jwt.sign({ nickname }, 'token');
      res.send({ token });
    }
  });
});

app.post('/students', jsonParser, (req, res) => {
  const { nickname, name, surname } = req.body;
  const authHeader = req.headers.authorization;
  const token = authHeader.split(' ')[1];
  jwt.verify(token, 'token', (err, decoded) => {
    if (err) {
      res.status(401).send('Error: user is unauthorized');
    } else {
      pool.query('INSERT INTO students (nickname, name, surname) VALUES ($1, $2, $3)', [nickname, name, surname], (err) => {
        if (err) {
          res.status(500).send(err.message);
        } else {
          res.send('Created successfully');
        }
      });
    }
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
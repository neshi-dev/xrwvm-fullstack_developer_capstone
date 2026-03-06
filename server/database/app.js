/*jshint esversion: 8 */
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.json());

// Load data from JSON files into memory
let reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'))['reviews'];
let dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'))['dealerships'];

console.log(`Loaded ${dealerships_data.length} dealerships and ${reviews_data.length} reviews from JSON files.`);

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Dealers API")
});

// Fetch all reviews
app.get('/fetchReviews', (req, res) => {
  res.json(reviews_data);
});

// Fetch reviews by dealer id
app.get('/fetchReviews/dealer/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const result = reviews_data.filter(r => r.dealership === id);
  res.json(result);
});

// Fetch all dealerships
app.get('/fetchDealers', (req, res) => {
  res.json(dealerships_data);
});

// Fetch dealers by state
app.get('/fetchDealers/:state', (req, res) => {
  const state = req.params.state;
  const result = dealerships_data.filter(d => d.state === state);
  res.json(result);
});

// Fetch dealer by id
app.get('/fetchDealer/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const dealer = dealerships_data.find(d => d.id === id);
  res.json(dealer ? [dealer] : []);
});

// Insert review (in-memory only, sufficient for screenshots)
app.post('/insert_review', (req, res) => {
  try {
    let data;
    if (Buffer.isBuffer(req.body) || typeof req.body === 'string') {
      data = JSON.parse(req.body);
    } else {
      data = req.body;
    }
    const maxId = reviews_data.reduce((m, r) => Math.max(m, r.id), 0);
    const review = {
      id: maxId + 1,
      name: data['name'],
      dealership: parseInt(data['dealership']),
      review: data['review'],
      purchase: data['purchase'],
      purchase_date: data['purchase_date'],
      car_make: data['car_make'],
      car_model: data['car_model'],
      car_year: data['car_year'],
    };
    reviews_data.push(review);
    res.json(review);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

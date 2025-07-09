const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/todo_db', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Define Todo schema
const todoSchema = new mongoose.Schema({
  task: String,
  created_at: { type: Date, default: Date.now },
});

const Todo = mongoose.model('Todo', todoSchema);

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes

// GET '/' - show all todos
app.get('/', async (req, res) => {
  const todos = await Todo.find().sort({ created_at: -1 });
  res.render('index', { todos });
});

// POST '/add' - add a todo
app.post('/add', async (req, res) => {
  const todoText = req.body.todo;
  if (todoText) {
    await Todo.create({ task: todoText });
  }
  res.redirect('/');
});

// GET '/delete/:id' - delete a todo by id
app.get('/delete/:id', async (req, res) => {
  const id = req.params.id;
  await Todo.findByIdAndDelete(id);
  res.redirect('/');
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server started on http://localhost:${PORT}`);
});

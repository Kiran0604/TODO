from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
todos = client.todo_db.todos

@app.route('/')
def index():
    return render_template('index.html', todos=todos.find())

@app.route('/add', methods=['POST'])
def add():
    todo = request.form.get('todo')
    if todo:
        todos.insert_one({'task': todo, 'created_at': datetime.now()})
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    todos.delete_one({'_id': ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

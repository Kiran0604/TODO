from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId  # ✅ Required for ObjectId casting

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.todo_db
todos = db.todos

@app.route('/')
def index():
    all_todos = list(todos.find())
    return render_template('index.html', todos=all_todos)

@app.route('/add', methods=['POST'])
def add():
    todo_text = request.form.get('todo')
    if todo_text:
        todos.insert_one({'task': todo_text})
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    todos.delete_one({'_id': ObjectId(id)})  # ✅ Fixed here
    return redirect('/')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        new_task = request.form.get('todo')
        if new_task:
            todos.update_one({'_id': ObjectId(id)}, {'$set': {'task': new_task}})
        return redirect('/')
    else:
        todo = todos.find_one({'_id': ObjectId(id)})
        return render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)

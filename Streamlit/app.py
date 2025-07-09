import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.todo_db
todos = db.todos

st.set_page_config(page_title="TODO App", page_icon="✅")
st.title("📝 TODO App with MongoDB")

# Add Task
with st.form("add_form", clear_on_submit=True):
    task = st.text_input("Enter a new task:")
    submitted = st.form_submit_button("Add")
    if submitted and task:
        todos.insert_one({"task": task})
        st.success("Task added!")

# Display Tasks
st.subheader("Your Tasks")
all_tasks = list(todos.find())
for todo in all_tasks:
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.write(f"• {todo['task']}")
    with col2:
        if st.button("❌", key=str(todo["_id"])):
            todos.delete_one({"_id": ObjectId(todo["_id"])})
            st.rerun()

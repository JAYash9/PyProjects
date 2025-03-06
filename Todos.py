import streamlit as st
import functions as fn
st.title('To-Do List')
st.header('Add your task ')
todos=fn.get_todos()
def add_todos():
    todo=st.session_state["new_todo"]+"\n"
    todos.append(todo)
    fn.write_todos(todos)

for index, todo in enumerate(todos):
    checklist=st.checkbox(key=index, label=todo)
    if checklist:
        todos.pop(index)
        fn.write_todos(todos)
        del st.session_state[index]
        st.rerun()
    
st.text_input(label="Add",placeholder='Add your task',on_change=add_todos,key='new_todo')

# st.session_state
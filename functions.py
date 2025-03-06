def get_todos(filepath="todos.txt"):
    with open(filepath,"r") as file_local:
        todolocal=file_local.readlines()
    return todolocal
def write_todos(todo_arg,filepath="todos.txt"):
    with open(filepath,"w") as file:
        file.writelines(todo_arg)
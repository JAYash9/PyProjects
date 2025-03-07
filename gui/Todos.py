import functions
import FreeSimpleGUI as fsg
label=fsg.Text("Welcome to Todos")
input_box=fsg.InputText(tooltip="Enter a new todo")
add_button=fsg.Button("Add",tooltip="Add a new todo")
window=fsg.Window("Todos",layout=[[label],[input_box,add_button]])
window.read()
window.close()
# while True:
#     user_action = input("type add, show, edit, complete or exit: ")
#     user_action = user_action.strip()

#     if user_action.startswith("add"):   
#         todo = user_action[4:]
#         todos = functions.get_todos()
#         todos.append(todo + "\n")
#         functions.write_todos(todos)
#     elif user_action.startswith("show"):
#         todos = functions.get_todos()
#         for index, i in enumerate(todos):
#             i = i.strip("\n")
#             row = f"{index + 1} - {i}"
#             print(row)
#     elif user_action.startswith("edit"):
#         try:
#             number = int(user_action[5:])
#             number = number - 1
#             todos = functions.get_todos()
#             new_todo = input("Enter a new todo:")
#             todos[number] = new_todo + "\n"
#             functions.write_todos(todos)
#         except ValueError:
#             print("command is not valid")
#             continue

#     elif user_action.startswith("complete"):
#         try:
#             number = int(user_action[9:])
#             todos = functions.get_todos()
#             index = number - 1
#             todo_to_remove = todos[index].strip("\n")
#             todos.pop(index)
#             functions.write_todos(todos)
#             message = f"Todo{index} was removed from the list"
#             print(message)
#         except IndexError:
#             print("Command is not valid")
#             continue
#     elif user_action.startswith("exit"):
#         break
#     else:
#         print("Command is not valid")
# print("Bye")

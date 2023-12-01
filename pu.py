import tkinter as tk
from tkinter import simpledialog, messagebox
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_FILE = 'todo_lists.json'

def load_lists():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_lists(lists):
    with open(DATA_FILE, 'w') as file:
        json.dump(lists, file)

def add_list():
    list_name = simpledialog.askstring("Input", "Enter the new list name:", parent=window)
    if list_name:
        lists[list_name] = []
        save_lists(lists)
        update_listbox()

def add_item_to_list(list_name, item):
    lists[list_name].append(item)
    save_lists(lists)

def delete_list():
    list_name = listbox.get(tk.ACTIVE)
    if list_name and messagebox.askyesno("Confirm", f"Are you sure you want to delete '{list_name}'?"):
        del lists[list_name]
        save_lists(lists)
        update_listbox()

def show_items(event):
    list_name = listbox.get(listbox.curselection())
    if list_name:
        items_window = tk.Toplevel(window)
        items_window.title(f"Items in {list_name}")

        items_listbox = tk.Listbox(items_window)
        items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for item in lists[list_name]:
            items_listbox.insert(tk.END, item)

        def add_item():
            item = simpledialog.askstring("Input", f"Enter a new item for list '{list_name}':", parent=items_window)
            if item:
                add_item_to_list(list_name, item)
                items_listbox.insert(tk.END, item)

        def delete_item():
            selected_index = items_listbox.curselection()
            if selected_index:
                items_listbox.delete(selected_index)
                del lists[list_name][selected_index[0]]
                save_lists(lists)

        def move_item_up():
            selected_index = items_listbox.curselection()
            if selected_index and selected_index[0] > 0:
                item = lists[list_name].pop(selected_index[0])
                lists[list_name].insert(selected_index[0] - 1, item)
                save_lists(lists)
                update_items_listbox()

        def move_item_down():
            selected_index = items_listbox.curselection()
            if selected_index and selected_index[0] < len(lists[list_name]) - 1:
                item = lists[list_name].pop(selected_index[0])
                lists[list_name].insert(selected_index[0] + 1, item)
                save_lists(lists)
                update_items_listbox()

        def update_items_listbox():
            items_listbox.delete(0, tk.END)
            for item in lists[list_name]:
                items_listbox.insert(tk.END, item)

        btn_frame = tk.Frame(items_window)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

        add_item_button = tk.Button(btn_frame, text="Add Item", command=add_item)
        add_item_button.pack()

        delete_item_button = tk.Button(btn_frame, text="Delete Item", command=delete_item)
        delete_item_button.pack()

        move_up_button = tk.Button(btn_frame, text="Move Up", command=move_item_up)
        move_up_button.pack()

        move_down_button = tk.Button(btn_frame, text="Move Down", command=move_item_down)
        move_down_button.pack()

def update_listbox():
    listbox.delete(0, tk.END)
    for name in lists:
        listbox.insert(tk.END, name)

def save_as_pdf(list_name, items):
    pass

window = tk.Tk()
window.title("To-Do List Application")

listbox = tk.Listbox(window)
listbox.pack()
listbox.bind('<Double-Button-1>', show_items)

add_list_button = tk.Button(window, text="Add New List", command=add_list)
add_list_button.pack()

delete_list_button = tk.Button(window, text="Delete List", command=delete_list)
delete_list_button.pack()

lists = load_lists()
update_listbox()

window.mainloop()

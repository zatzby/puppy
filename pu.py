import tkinter as tk
from tkinter import simpledialog, messagebox
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_FILE = 'todo_lists.json'

# Load lists from file
def load_lists():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save lists to file
def save_lists(lists):
    with open(DATA_FILE, 'w') as file:
        json.dump(lists, file)

# Add new list
def add_list():
    list_name = simpledialog.askstring("Input", "Enter the new list name:", parent=window)
    if list_name:
        lists[list_name] = []
        save_lists(lists)
        update_listbox()

# Add item to list
def add_item_to_list(list_name, item):
    lists[list_name].append(item)
    save_lists(lists)

# Delete list
def delete_list():
    list_name = listbox.get(tk.ACTIVE)
    if list_name and messagebox.askyesno("Confirm", f"Are you sure you want to delete '{list_name}'?"):
        del lists[list_name]
        save_lists(lists)
        update_listbox()

# Show items of selected list
def show_items(event):
    list_name = listbox.get(listbox.curselection())
    if list_name:
        items_window = tk.Toplevel(window)
        items_window.title(f"Items in {list_name}")

        items_listbox = tk.Listbox(items_window)
        items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for item in lists[list_name]:
            items_listbox.insert(tk.END, item)

        # Add item
        def add_item():
            item = simpledialog.askstring("Input", f"Enter a new item for list '{list_name}':", parent=items_window)
            if item:
                add_item_to_list(list_name, item)
                items_listbox.insert(tk.END, item)

        # Delete item
        def delete_item():
            selected_index = items_listbox.curselection()
            if selected_index:
                items_listbox.delete(selected_index)
                del lists[list_name][selected_index[0]]
                save_lists(lists)

        # Move item up
        def move_item_up():
            selected_index = items_listbox.curselection()
            if selected_index and selected_index[0] > 0:
                item = lists[list_name].pop(selected_index[0])
                lists[list_name].insert(selected_index[0] - 1, item)
                save_lists(lists)
                update_items_listbox()

        # Move item down
        def move_item_down():
            selected_index = items_listbox.curselection()
            if selected_index and selected_index[0] < len(lists[list_name]) - 1:
                item = lists[list_name].pop(selected_index[0])
                lists[list_name].insert(selected_index[0] + 1, item)
                save_lists(lists)
                update_items_listbox()

        # Update items listbox
        def update_items_listbox():
            items_listbox.delete(0, tk.END)
            for item in lists[list_name]:
                items_listbox.insert(tk.END, item)

        # Item management buttons
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

# Update main listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for name in lists:
        listbox.insert(tk.END, name)

# Placeholder for PDF saving
def save_as_pdf(list_name, items):
    pass

# Main window setup
window = tk.Tk()
window.title("To-Do List Application")
window.geometry("500x500")

# Main listbox
listbox = tk.Listbox(window)
listbox.pack()
listbox.bind('<Double-Button-1>', show_items)

# New list button
add_list_button = tk.Button(window, text="Add New List", command=add_list)
add_list_button.pack()

# Delete list button
delete_list_button = tk.Button(window, text="Delete List", command=delete_list)
delete_list_button.pack()

# Load and display lists
lists = load_lists()
update_listbox()

# Start application
window.mainloop()

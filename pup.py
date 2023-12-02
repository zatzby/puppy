import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_FILE = 'todo_lists.json'  # Path to the data file

# Load existing lists from the data file
def load_lists():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save current lists to the data file
def save_lists(lists):
    with open(DATA_FILE, 'w') as file:
        json.dump(lists, file)

# Function to add a new list
def add_list():
    list_name = simpledialog.askstring("Input", "Enter the new list name:", parent=window)
    if list_name:
        lists[list_name] = []
        save_lists(lists)
        update_listbox()
        show_items_for_list(list_name)

# Function to add an item to a specific list
def add_item_to_list(list_name, item):
    lists[list_name].append(item)
    save_lists(lists)

# Function to delete a selected list
def delete_list():
    list_name = listbox.get(tk.ACTIVE)
    if list_name and messagebox.askyesno("Confirm", f"Are you sure you want to delete '{list_name}'?"):
        del lists[list_name]
        save_lists(lists)
        update_listbox()

# Function to save a list as a PDF file
def save_as_pdf(list_name, items):
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 14)
        c.drawCentredString(300, 750, f"Job Name: {list_name}")
        current_date = datetime.datetime.now().strftime("%m/%d/%y")
        c.drawString(500, 750, current_date)
        y = 730
        for i, item in enumerate(items, start=1):
            c.drawString(72, y, f"{i}. {item}")
            y -= 28
        c.save()

# Function to show items of a selected list in a new window
def show_items_for_list(list_name):
    items_window = tk.Toplevel(window)
    items_window.title(f"Items in {list_name}")

    items_listbox = tk.Listbox(items_window)
    items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for item in lists.get(list_name, []):
        items_listbox.insert(tk.END, item)

    # Predefined phrases for quick addition
    predefined_phrases = ["Phrase 1", "Phrase 2", "Phrase 3", "Phrase 4"]

    # Function to open window for selecting predefined phrases
    def open_phrase_window():
        phrase_window = tk.Toplevel(items_window)
        phrase_window.title("Select a Predefined Phrase")
        phrase_listbox = tk.Listbox(phrase_window)
        phrase_listbox.pack()

        for phrase in predefined_phrases:
            phrase_listbox.insert(tk.END, phrase)

        def add_selected_phrase():
            selected_phrase = phrase_listbox.get(tk.ACTIVE)
            if selected_phrase:
                add_item_to_list(list_name, selected_phrase)
                items_listbox.insert(tk.END, selected_phrase)
                phrase_window.destroy()

        add_phrase_button = tk.Button(phrase_window, text="Add to List", command=add_selected_phrase)
        add_phrase_button.pack()

    # Frame for item management buttons
    btn_frame = tk.Frame(items_window)
    btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

    # Buttons for different functionalities
    add_item_button = tk.Button(btn_frame, text="Add Item", command=lambda: add_item(list_name, items_listbox))
    add_item_button.pack()

    delete_item_button = tk.Button(btn_frame, text="Delete Item", command=lambda: delete_item(items_listbox))
    delete_item_button.pack()

    move_up_button = tk.Button(btn_frame, text="Move Up", command=lambda: move_item_up(items_listbox))
    move_up_button.pack()

    move_down_button = tk.Button(btn_frame, text="Move Down", command=lambda: move_item_down(items_listbox))
    move_down_button.pack()

    save_pdf_button = tk.Button(btn_frame, text="Save as PDF", command=lambda: save_as_pdf(list_name, lists[list_name]))
    save_pdf_button.pack()

    select_phrase_button = tk.Button(btn_frame, text="Select Phrase", command=open_phrase_window)
    select_phrase_button.pack()

    # Functions for adding, deleting, moving items and updating listbox
    def add_item(list_name, items_listbox):
        item = simpledialog.askstring("Input", f"Enter a new item for list '{list_name}':", parent=items_window)
        if item:
            add_item_to_list(list_name, item)
            items_listbox.insert(tk.END, item)

    def delete_item(items_listbox):
        selected_index = items_listbox.curselection()
        if selected_index:
            del lists[list_name][selected_index[0]]
            save_lists(lists)
            update_items_listbox(items_listbox)

    def move_item_up(items_listbox):
        selected_index = items_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            item = lists[list_name].pop(selected_index[0])
            lists[list_name].insert(selected_index[0] - 1, item)
            save_lists(lists)
            update_items_listbox(items_listbox)

    def move_item_down(items_listbox):
        selected_index = items_listbox.curselection()
        if selected_index and selected_index[0] < len(lists[list_name]) - 1:
            item = lists[list_name].pop(selected_index[0])
            lists[list_name].insert(selected_index[0] + 1, item)
            save_lists(lists)
            update_items_listbox(items_listbox)

    def update_items_listbox(items_listbox):
        items_listbox.delete(0, tk.END)
        for item in lists[list_name]:
            items_listbox.insert(tk.END, item)

def show_items(event):
    list_name = listbox.get(listbox.curselection())
    if list_name:
        show_items_for_list(list_name)

def update_listbox():
    listbox.delete(0, tk.END)
    for name in lists:
        listbox.insert(tk.END, name)

# Main application setup
window = tk.Tk()
window.title("To-Do List Application")
window.geometry("400x400")

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

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_FILE = 'todo_lists.json'  # File for storing list data

# Load lists from JSON file
def load_lists():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save lists to JSON file
def save_lists(lists):
    with open(DATA_FILE, 'w') as file:
        json.dump(lists, file)

# Add a new list
def add_list():
    list_name = simpledialog.askstring("Input", "Enter the new list name:", parent=window)
    if list_name:
        lists[list_name] = []
        save_lists(lists)
        update_listbox()

# Add an item to a specific list
def add_item_to_list(list_name, item):
    lists[list_name].append(item)
    save_lists(lists)

# Delete a selected list
def delete_list():
    list_name = listbox.get(tk.ACTIVE)
    if list_name and messagebox.askyesno("Confirm", f"Are you sure you want to delete '{list_name}'?"):
        del lists[list_name]
        save_lists(lists)
        update_listbox()

# Save list as a PDF file
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
            c.drawString(100, y, f"{i}. {item}")
            y -= 20
        c.save()

# Show items of a selected list in a new window
def show_items(event):
    list_name = listbox.get(listbox.curselection())
    if list_name:
        items_window = tk.Toplevel(window)
        items_window.title(f"Items in {list_name}")

        items_listbox = tk.Listbox(items_window)
        items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for item in lists[list_name]:
            items_listbox.insert(tk.END, item)

        predefined_phrases = ["Phrase 1", "Phrase 2", "Phrase 3", "Phrase 4"]

        # Open window for phrase selection
        def open_phrase_window():
            phrase_window = tk.Toplevel(items_window)
            phrase_window.title("Select a Predefined Phrase")
            phrase_listbox = tk.Listbox(phrase_window)
            phrase_listbox.pack()

            for phrase in predefined_phrases:
                phrase_listbox.insert(tk.END, phrase)

            # Add selected phrase to list
            def add_selected_phrase():
                selected_phrase = phrase_listbox.get(tk.ACTIVE)
                if selected_phrase:
                    add_item_to_list(list_name, selected_phrase)
                    items_listbox.insert(tk.END, selected_phrase)
                    phrase_window.destroy()

            add_phrase_button = tk.Button(phrase_window, text="Add to List", command=add_selected_phrase)
            add_phrase_button.pack()

        # Buttons for item management
        btn_frame = tk.Frame(items_window)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

        save_pdf_button = tk.Button(btn_frame, text="Save as PDF", command=lambda: save_as_pdf(list_name, lists[list_name]))
        save_pdf_button.pack()

        select_phrase_button = tk.Button(btn_frame, text="Select Phrase", command=open_phrase_window)
        select_phrase_button.pack()

        add_item_button = tk.Button(btn_frame, text="Add Item", command=lambda: add_item())
        add_item_button.pack()

        delete_item_button = tk.Button(btn_frame, text="Delete Item", command=lambda: delete_item())
        delete_item_button.pack()

        move_up_button = tk.Button(btn_frame, text="Move Up", command=lambda: move_item_up())
        move_up_button.pack()

        move_down_button = tk.Button(btn_frame, text="Move Down", command=lambda: move_item_down())
        move_down_button.pack()

        # Functions for managing items in a list
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

# Update the main listbox with list names
def update_listbox():
    listbox.delete(0, tk.END)
    for name in lists:
        listbox.insert(tk.END, name)

# Main application window setup
window = tk.Tk()
window.title("To-Do List Application")
window.geometry("400x400")

# Main list display
listbox = tk.Listbox(window)
listbox.pack()
listbox.bind('<Double-Button-1>', show_items)

# Buttons for adding and deleting lists
add_list_button = tk.Button(window, text="Add New List", command=add_list)
add_list_button.pack()

delete_list_button = tk.Button(window, text="Delete List", command=delete_list)
delete_list_button.pack()

# Load lists from file and display
lists = load_lists()
update_listbox()

window.mainloop()
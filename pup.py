import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image, ImageTk

DATA_FILE = 'puppy_lists.json'  

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
        show_items_for_list(list_name)

def add_item_to_list(list_name, item):
    lists[list_name].append(item)
    save_lists(lists)

def delete_list():
    list_name = listbox.get(tk.ACTIVE)
    if list_name and messagebox.askyesno("Confirm", f"Are you sure you want to delete '{list_name}'?"):
        del lists[list_name]
        save_lists(lists)
        update_listbox()

def edit_item(list_name, items_listbox, items_window):
    selected_index = items_listbox.curselection()
    if selected_index:
        current_item = lists[list_name][selected_index[0]]
        new_item = simpledialog.askstring("Edit Item", f"Edit the item '{current_item}':", initialvalue=current_item, parent=items_window)
        if new_item:
            lists[list_name][selected_index[0]] = new_item
            save_lists(lists)
            update_items_listbox(items_listbox, list_name)
            items_listbox.selection_set(selected_index)
            items_listbox.see(selected_index)
            items_listbox.focus_set()

def save_as_pdf(list_name, items):
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 14)
        c.drawCentredString(300, 750, f"Pickup at {list_name}")
        current_date = datetime.datetime.now().strftime("%m/%d/%y")
        c.drawString(500, 750, current_date)
        y = 700
        for i, item in enumerate(items, start=1):
            c.drawString(72, y, f"{item}")
            y -= 50
        c.save()

def show_items_for_list(list_name):
    items_window = tk.Toplevel(window)
    items_window.geometry("600x600")
    items_window.title(f"{list_name}")

    items_listbox = tk.Listbox(items_window)
    items_listbox.bind('<Double-Button-1>', lambda event: show_items(event, list_name))
    items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    update_items_listbox(items_listbox, list_name)
    
    items_window.bind('<a>', lambda event: add_item(list_name, items_listbox))
    items_window.bind('<d>', lambda event: delete_item(list_name, items_listbox))
    items_window.bind('<w>', lambda event: move_item_up(list_name, items_listbox))
    items_window.bind('<s>', lambda event: move_item_down(list_name, items_listbox))
    items_window.bind('<e>', lambda event: edit_item(list_name, items_listbox, items_window))
    items_window.bind('<o>', lambda event: open_common_items_window())
    items_window.bind('<p>', lambda event: save_as_pdf(list_name, lists[list_name]))

    predefined_common_items = ["Common item 1", "Common item 2", "Common item 3", "Common item 4"]

    def open_common_items_window():
        common_items_window = tk.Toplevel(items_window)
        common_items_window.geometry("500x500")
        common_items_window.title("Select an item to add to list")
        common_items_listbox = tk.Listbox(common_items_window)
        common_items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for common_item in predefined_common_items:
            common_items_listbox.insert(tk.END, common_item)

        def add_selected_common_item():
            common_item = common_items_listbox.get(tk.ACTIVE)
            if common_item:
                add_item_to_list(list_name, common_item)
                update_items_listbox(items_listbox, list_name)
                common_items_window.destroy()

        add_common_item_button = tk.Button(common_items_window, text="Add to List", command=add_selected_common_item)
        add_common_item_button.pack()

        common_items_window.focus_set()
        common_items_listbox.focus_set()

    btn_frame = tk.Frame(items_window)
    btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

    add_item_button = tk.Button(btn_frame, text="Add Item", underline=0, command=lambda: add_item(list_name, items_listbox))
    add_item_button.pack()

    delete_item_button = tk.Button(btn_frame, text="Delete Item", underline=0, command=lambda: delete_item(list_name, items_listbox))
    delete_item_button.pack()

    move_up_button = tk.Button(btn_frame, text="Move Up", command=lambda: move_item_up(list_name, items_listbox))
    move_up_button.pack()

    move_down_button = tk.Button(btn_frame, text="Move Down", command=lambda: move_item_down(list_name, items_listbox))
    move_down_button.pack()

    edit_item_button = tk.Button(btn_frame, text="Edit Item", underline=0, command=lambda: edit_item(list_name, items_listbox, items_window))
    edit_item_button.pack()

    select_common_item_button = tk.Button(btn_frame, text="Select Item", underline=0, command=open_common_items_window)
    select_common_item_button.pack()

    save_pdf_button = tk.Button(btn_frame, text="Save as PDF", underline=8, command=lambda: save_as_pdf(list_name, lists[list_name]))
    save_pdf_button.pack()

    items_window.focus_set()
    items_listbox.focus_set()

def add_item(list_name, items_listbox):
    item = simpledialog.askstring("Input", f"Enter a new item for list '{list_name}':", parent=items_listbox.master)
    if item:
        add_item_to_list(list_name, item)
        update_items_listbox(items_listbox, list_name)
        items_listbox.selection_clear(0, tk.END)
        items_listbox.selection_set(tk.END)
        items_listbox.see(tk.END)
        items_listbox.focus_set()

def delete_item(list_name, items_listbox):
    selected_index = items_listbox.curselection()
    if selected_index and messagebox.askyesno("Confirm", f"Are you sure you want to delete this item?"):
        del lists[list_name][selected_index[0]]
        save_lists(lists)
        update_items_listbox(items_listbox, list_name)
        
        items_listbox.after(10, lambda: set_focus_and_selection(items_listbox, list_name))

def set_focus_and_selection(items_listbox, list_name):
    items_listbox.focus_set()
    if lists[list_name]:  
        items_listbox.selection_set(0)  
        items_listbox.see(0)  
    else:
        items_listbox.selection_clear(0, tk.END) 
    
    items_listbox.master.focus_force()

def move_item_up(list_name, items_listbox):
    selected_index = items_listbox.curselection()
    if selected_index and selected_index[0] > 0:
        item = lists[list_name].pop(selected_index[0])
        new_index = selected_index[0] - 1
        lists[list_name].insert(new_index, item)
        save_lists(lists)
        update_items_listbox(items_listbox, list_name)
        items_listbox.selection_set(new_index)
        items_listbox.see(new_index)
        items_listbox.focus_set()

def move_item_down(list_name, items_listbox):
    selected_index = items_listbox.curselection()
    if selected_index and selected_index[0] < len(lists[list_name]) - 1:
        item = lists[list_name].pop(selected_index[0])
        new_index = selected_index[0] + 1
        lists[list_name].insert(new_index, item)
        save_lists(lists)
        update_items_listbox(items_listbox, list_name)
        items_listbox.selection_set(new_index)
        items_listbox.see(new_index)
        items_listbox.focus_set()

def update_items_listbox(items_listbox, list_name):
    items_listbox.delete(0, tk.END)
    for item in lists[list_name]:
        items_listbox.insert(tk.END, item)

def show_items(event, list_name):
    show_items_for_list(list_name)

def update_listbox():
    listbox.delete(0, tk.END)
    for name in lists:
        listbox.insert(tk.END, name)

window = tk.Tk()
window.title("Puppy List Maker")
window.geometry("600x600")

window.bind('<a>', lambda event: add_list())
window.bind('<d>', lambda event: delete_list())

#change path when switching OS
original_image = Image.open("puppy_logo.png")
resized_image = original_image.resize((150, 150), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(resized_image)

image_label = tk.Label(window, image=image)
image_label.pack(side=tk.TOP, anchor=tk.N)

listbox = tk.Listbox(window)
listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
listbox.bind('<Double-Button-1>', lambda event: show_items(event, listbox.get(listbox.curselection())))

add_list_button = tk.Button(window, text="Add New List", underline=0, command=add_list)
add_list_button.pack()

delete_list_button = tk.Button(window, text="Delete List", underline=0, command=delete_list)
delete_list_button.pack(pady=10)

lists = load_lists()
update_listbox()

window.mainloop()
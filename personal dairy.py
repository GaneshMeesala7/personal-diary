import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Database setup
conn = sqlite3.connect('basic_diary.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                content TEXT)''')
conn.commit()

# Function to add a new diary entry
def add_entry():
    content = text_box.get("1.0", "end-1c").strip()  # Get content from the Text widget and trim whitespace
    if content == "":
        messagebox.showwarning("Empty Entry", "Diary entry cannot be empty!")
        return
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO entries (date, content) VALUES (?, ?)", (date, content))
    conn.commit()  # Commit after inserting
    text_box.delete("1.0", END)  # Clear the text box
    refresh_entries()  # Refresh the displayed entries

# Function to refresh and show diary entries
def refresh_entries():
    entries_listbox.delete(*entries_listbox.get_children())  # Clear previous items
    c.execute("SELECT id, date, content FROM entries")
    rows = c.fetchall()
    
    if rows:  # Check if any rows are fetched
        for row in rows:
            entries_listbox.insert('', 'end', values=(row[1], row[2]))  # Display the date and content
    else:
        entries_listbox.insert('', 'end', values=("No entries available", ""))  # Show a placeholder if no entries exist

# Function to delete a selected entry
def delete_entry():
    selected_item = entries_listbox.selection()  # Get the selected row ID
    if not selected_item:
        messagebox.showwarning("Select an Entry", "Please select an entry to delete!")
        return

    selected_date = entries_listbox.item(selected_item, 'values')[0]  # Extract the date from the selected entry

    # Find the ID of the selected entry in the database using the date
    c.execute("SELECT id FROM entries WHERE date = ?", (selected_date,))
    entry_id = c.fetchone()

    if entry_id:
        # Delete the selected entry from the database
        c.execute("DELETE FROM entries WHERE id = ?", (entry_id[0],))
        conn.commit()  # Commit after deleting

        # Refresh the entry list
        refresh_entries()
    else:
        messagebox.showerror("Error", "Failed to delete entry")

# GUI Setup
root = Tk()
root.title("Personal Diary")

# Styling
root.configure(bg='#f0f0f0')
root.geometry("500x500")
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
style.configure("Treeview", font=("Arial", 10), rowheight=25)

# Add a heading
Label(root, text="Personal Diary", font=("Arial", 18, "bold"), bg='#f0f0f0', pady=10).pack()

# Add entry text box
Label(root, text="Enter your message:", font=("Arial", 12), bg='#f0f0f0').pack(pady=5)
text_box = Text(root, height=5, width=50, font=("Arial", 12))
text_box.pack(pady=5)

# Add entry button
Button(root, text="Add Entry", command=add_entry, font=("Arial", 12, "bold"), bg='#008CBA', fg='white').pack(pady=10)

# Listbox to show diary entries with a Scrollbar
Label(root, text="Messages:", font=("Arial", 12), bg='#f0f0f0').pack(pady=5)

# Create a Treeview (table) to display the entries
columns = ('date', 'content')
entries_listbox = ttk.Treeview(root, columns=columns, show='headings', height=8)
entries_listbox.heading('date', text='Date & Time')
entries_listbox.heading('content', text='Message')
entries_listbox.pack(pady=10, padx=10, fill=BOTH, expand=True)

# Add a scrollbar to the Treeview
scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=entries_listbox.yview)
entries_listbox.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

# Delete entry button
Button(root, text="Delete Selected Entry", command=delete_entry, font=("Arial", 12, "bold"), bg='#f44336', fg='white').pack(pady=5)

# Show entries when the app starts
refresh_entries()

root.mainloop()

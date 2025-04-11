#!/usr/bin/env python
# coding: utf-8

# In[6]:


def calculate_real_size(microscope_size, magnification):
    return microscope_size / magnification


# In[7]:


import sqlite3

def create_db():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS specimens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        microscope_size REAL,
        magnification REAL,
        actual_size REAL
    )
    """)
    conn.commit()
    conn.close()

def save_record(username, microscope_size, magnification, actual_size):
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO specimens (username, microscope_size, magnification, actual_size) VALUES (?, ?, ?, ?)",
                   (username, microscope_size, magnification, actual_size))
    conn.commit()
    conn.close()


# In[8]:


if __name__ == "__main__":
    create_db()
    username = input("Enter username: ")
    microscope_size = float(input("Enter microscope size (mm): "))
    magnification = float(input("Enter magnification: "))
    actual_size = calculate_real_size(microscope_size, magnification)
    save_record(username, microscope_size, magnification, actual_size)
    print(f"Real-life size: {actual_size:.2f} mm")


# In[10]:


import tkinter as tk
from tkinter import messagebox

def gui_app():
    create_db()

    def calculate_and_save():
        try:
            username = username_entry.get()
            size = float(size_entry.get())
            mag = float(mag_entry.get())
            actual = calculate_real_size(size, mag)
            save_record(username, size, mag, actual)
            result_label.config(text=f"Real-life size: {actual:.2f} mm")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    root = tk.Tk()
    root.title("Microscope Specimen Size Calculator")

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Microscope Size (mm)").pack()
    size_entry = tk.Entry(root)
    size_entry.pack()

    tk.Label(root, text="Magnification").pack()
    mag_entry = tk.Entry(root)
    mag_entry.pack()

    tk.Button(root, text="Calculate", command=calculate_and_save).pack()
    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

# Run GUI
if __name__ == "__main__":
    gui_app()


# In[11]:


pip install flask


# In[ ]:


from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_db():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS specimens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        microscope_size REAL,
        magnification REAL,
        actual_size REAL
    )
    """)
    conn.commit()
    conn.close()

def save_record(username, microscope_size, magnification, actual_size):
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO specimens (username, microscope_size, magnification, actual_size) VALUES (?, ?, ?, ?)",
                   (username, microscope_size, magnification, actual_size))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        microscope_size = float(request.form['microscope_size'])
        magnification = float(request.form['magnification'])
        actual_size = microscope_size / magnification
        save_record(username, microscope_size, magnification, actual_size)
        return render_template('index.html', result=f"Real-life size: {actual_size:.2f} mm")
    return render_template('index.html')

if __name__ == '__main__':
    create_db()
    app.run(debug=True)


import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os


# =========================
# COLORS
# =========================

LIGHT_BG = "#F5F7FA"
LIGHT_SIDEBAR = "#E9EDF3"
LIGHT_WHITE = "#FFFFFF"
LIGHT_TEXT = "#202124"
LIGHT_BUTTON = "#4F46E5"

DARK_BG = "#18181B"
DARK_SIDEBAR = "#27272A"
DARK_WHITE = "#27272A"
DARK_TEXT = "#F4F4F5"
DARK_BUTTON = "#6366F1"


# =========================
# APP WINDOW
# =========================

root = tk.Tk()
root.title("My Notes")
root.geometry("1000x600")
root.minsize(800, 500)

dark_mode = False
notes = []
filtered_indexes = []


# =========================
# NOTES FILE LOCATION
# =========================

app_folder = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")),
    "My Notes"
)

os.makedirs(app_folder, exist_ok=True)

notes_file = os.path.join(app_folder, "my_notes.txt")


# =========================
# SAVE NOTES TO FILE
# =========================

def write_notes_to_file():

    with open(notes_file, "w", encoding="utf-8") as file:

        for note in notes:

            file.write("TITLE:" + note["title"] + "\n")
            file.write("DATE:" + note["date"] + "\n")
            file.write("CONTENT:\n")
            file.write(note["content"] + "\n")
            file.write("-" * 50 + "\n")


# =========================
# LOAD NOTES
# =========================

def load_notes():

    notes.clear()
    notes_list.delete(0, tk.END)

    if not os.path.exists(notes_file):
        return

    with open(notes_file, "r", encoding="utf-8") as file:
        data = file.read()

    blocks = data.split("-" * 50)

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        lines = block.split("\n")

        title = ""
        date = ""
        content = []

        reading_content = False

        for line in lines:

            if line.startswith("TITLE:"):
                title = line[6:]

            elif line.startswith("DATE:"):
                date = line[5:]

            elif line == "CONTENT:":
                reading_content = True

            elif reading_content:
                content.append(line)

        notes.append({
            "title": title,
            "date": date,
            "content": "\n".join(content)
        })

        notes_list.insert(tk.END, title)


# =========================
# REFRESH NOTES LIST
# =========================

def refresh_notes_list():

    global filtered_indexes

    notes_list.delete(0, tk.END)

    filtered_indexes = []

    search_text = search_entry.get().lower().strip()

    for index, note in enumerate(notes):

        if (
            search_text == ""
            or search_text in note["title"].lower()
            or search_text in note["content"].lower()
        ):

            filtered_indexes.append(index)
            notes_list.insert(tk.END, note["title"])


# =========================
# SAVE NOTE
# =========================

def save_note():

    title = title_entry.get().strip()
    content = text_box.get("1.0", tk.END).strip()

    if not title:
        messagebox.showwarning(
            "Missing Title",
            "Please enter a title for your note."
        )
        return

    if not content:
        messagebox.showwarning(
            "Empty Note",
            "Please write something in your note."
        )
        return

    selected = notes_list.curselection()

    if selected:

        display_index = selected[0]

        if search_entry.get().strip():
            actual_index = filtered_indexes[display_index]
        else:
            actual_index = display_index

        notes[actual_index]["title"] = title
        notes[actual_index]["content"] = content
        notes[actual_index]["date"] = datetime.now().strftime(
            "%d %B %Y, %I:%M %p"
        )

    else:

        notes.append({
            "title": title,
            "date": datetime.now().strftime(
                "%d %B %Y, %I:%M %p"
            ),
            "content": content
        })

    write_notes_to_file()
    refresh_notes_list()

    messagebox.showinfo(
        "Saved",
        "Your note has been saved successfully!"
    )


# =========================
# OPEN NOTE
# =========================

def open_note(event=None):

    selected = notes_list.curselection()

    if not selected:
        return

    display_index = selected[0]

    if search_entry.get().strip():
        actual_index = filtered_indexes[display_index]
    else:
        actual_index = display_index

    note = notes[actual_index]

    title_entry.delete(0, tk.END)
    title_entry.insert(0, note["title"])

    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", note["content"])

    date_label.config(
        text="Last updated: " + note["date"]
    )

    update_counter()


# =========================
# NEW NOTE
# =========================

def new_note():

    notes_list.selection_clear(0, tk.END)

    title_entry.delete(0, tk.END)

    text_box.delete("1.0", tk.END)

    date_label.config(
        text="New note"
    )

    update_counter()

    title_entry.focus()


# =========================
# DELETE NOTE
# =========================

def delete_note():

    selected = notes_list.curselection()

    if not selected:
        messagebox.showwarning(
            "No Note Selected",
            "Please select a note to delete."
        )
        return

    answer = messagebox.askyesno(
        "Delete Note",
        "Are you sure you want to delete this note?"
    )

    if not answer:
        return

    display_index = selected[0]

    if search_entry.get().strip():
        actual_index = filtered_indexes[display_index]
    else:
        actual_index = display_index

    notes.pop(actual_index)

    write_notes_to_file()

    new_note()
    refresh_notes_list()


# =========================
# SEARCH
# =========================

def search_notes():

    refresh_notes_list()


def clear_search():

    search_entry.delete(0, tk.END)
    refresh_notes_list()


# =========================
# WORD + CHARACTER COUNTER
# =========================

def update_counter(event=None):

    content = text_box.get("1.0", tk.END).strip()

    characters = len(content)

    if content:
        words = len(content.split())
    else:
        words = 0

    counter_label.config(
        text=f"Words: {words}    Characters: {characters}"
    )


# =========================
# DARK MODE
# =========================

def toggle_dark_mode():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        bg = DARK_BG
        sidebar = DARK_SIDEBAR
        white = DARK_WHITE
        text = DARK_TEXT
        button = DARK_BUTTON

        dark_button.config(text="☀ Light Mode")

    else:

        bg = LIGHT_BG
        sidebar = LIGHT_SIDEBAR
        white = LIGHT_WHITE
        text = LIGHT_TEXT
        button = LIGHT_BUTTON

        dark_button.config(text="🌙 Dark Mode")

    root.configure(bg=bg)

    header.config(bg=bg, fg=text)

    sidebar_frame.config(bg=sidebar)
    sidebar_title.config(bg=sidebar, fg=text)

    editor_frame.config(bg=bg)

    title_entry.config(
        bg=white,
        fg=text,
        insertbackground=text
    )

    text_box.config(
        bg=white,
        fg=text,
        insertbackground=text
    )

    search_entry.config(
        bg=white,
        fg=text,
        insertbackground=text
    )

    notes_list.config(
        bg=white,
        fg=text,
        selectbackground=button,
        selectforeground="white"
    )

    date_label.config(
        bg=bg,
        fg=text
    )

    counter_label.config(
        bg=bg,
        fg=text
    )

    search_label.config(
        bg=bg,
        fg=text
    )

    sidebar_button_frame.config(bg=sidebar)

    for button_widget in [
        search_button,
        new_button,
        save_button,
        delete_button,
        dark_button
    ]:

        button_widget.config(
            bg=button,
            fg="white"
        )


# =========================
# KEYBOARD SHORTCUTS
# =========================

def keyboard_save(event=None):

    save_note()
    return "break"


def keyboard_new(event=None):

    new_note()
    return "break"


def keyboard_delete(event=None):

    delete_note()
    return "break"


root.bind("<Control-s>", keyboard_save)
root.bind("<Control-n>", keyboard_new)
root.bind("<Delete>", keyboard_delete)


# =========================
# CLOSE APP
# =========================

def close_app():

    answer = messagebox.askyesnocancel(
        "Exit My Notes",
        "Do you want to save before closing?"
    )

    if answer is None:
        return

    if answer:
        save_note()

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# =========================
# HEADER
# =========================

header = tk.Label(
    root,
    text="My Notes",
    font=("Segoe UI", 24, "bold"),
    bg=LIGHT_BG,
    fg=LIGHT_TEXT
)

header.pack(
    anchor="w",
    padx=25,
    pady=(20, 10)
)


# =========================
# SEARCH AREA
# =========================

search_frame = tk.Frame(
    root,
    bg=LIGHT_BG
)

search_frame.pack(
    fill="x",
    padx=25,
    pady=(0, 15)
)


search_label = tk.Label(
    search_frame,
    text="Search:",
    font=("Segoe UI", 11),
    bg=LIGHT_BG,
    fg=LIGHT_TEXT
)

search_label.pack(
    side="left"
)


search_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 11),
    width=35,
    bg=LIGHT_WHITE,
    fg=LIGHT_TEXT,
    relief="flat"
)

search_entry.pack(
    side="left",
    padx=8,
    ipady=6
)


search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_notes,
    bg=LIGHT_BUTTON,
    fg="white",
    relief="flat",
    padx=15,
    pady=5
)

search_button.pack(
    side="left"
)


clear_button = tk.Button(
    search_frame,
    text="Clear",
    command=clear_search,
    bg=LIGHT_SIDEBAR,
    fg=LIGHT_TEXT,
    relief="flat",
    padx=12,
    pady=5
)

clear_button.pack(
    side="left",
    padx=5
)


dark_button = tk.Button(
    search_frame,
    text="🌙 Dark Mode",
    command=toggle_dark_mode,
    bg=LIGHT_BUTTON,
    fg="white",
    relief="flat",
    padx=15,
    pady=5
)

dark_button.pack(
    side="right"
)


# =========================
# MAIN AREA
# =========================

main_frame = tk.Frame(
    root,
    bg=LIGHT_BG
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 20)
)


# =========================
# SIDEBAR
# =========================

sidebar_frame = tk.Frame(
    main_frame,
    bg=LIGHT_SIDEBAR,
    width=280
)

sidebar_frame.pack(
    side="left",
    fill="y"
)

sidebar_frame.pack_propagate(False)


sidebar_title = tk.Label(
    sidebar_frame,
    text="Your Notes",
    font=("Segoe UI", 14, "bold"),
    bg=LIGHT_SIDEBAR,
    fg=LIGHT_TEXT
)

sidebar_title.pack(
    anchor="w",
    padx=15,
    pady=15
)


notes_list = tk.Listbox(
    sidebar_frame,
    font=("Segoe UI", 11),
    bg=LIGHT_WHITE,
    fg=LIGHT_TEXT,
    selectbackground=LIGHT_BUTTON,
    selectforeground="white",
    relief="flat",
    activestyle="none"
)

notes_list.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10)
)

notes_list.bind(
    "<<ListboxSelect>>",
    open_note
)


# =========================
# SIDEBAR BUTTON
# =========================

sidebar_button_frame = tk.Frame(
    sidebar_frame,
    bg=LIGHT_SIDEBAR
)

sidebar_button_frame.pack(
    fill="x",
    padx=10,
    pady=(0, 10)
)


new_button = tk.Button(
    sidebar_button_frame,
    text="＋ New",
    command=new_note,
    bg=LIGHT_BUTTON,
    fg="white",
    relief="flat",
    pady=8
)

new_button.pack(
    fill="x"
)


# =========================
# EDITOR
# =========================

editor_frame = tk.Frame(
    main_frame,
    bg=LIGHT_BG
)

editor_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(20, 0)
)


title_entry = tk.Entry(
    editor_frame,
    font=("Segoe UI", 20, "bold"),
    bg=LIGHT_WHITE,
    fg=LIGHT_TEXT,
    relief="flat",
    insertbackground=LIGHT_TEXT
)

title_entry.pack(
    fill="x",
    ipady=10
)


date_label = tk.Label(
    editor_frame,
    text="New note",
    font=("Segoe UI", 9),
    bg=LIGHT_BG,
    fg="#6B7280"
)

date_label.pack(
    anchor="w",
    pady=(5, 10)
)


text_box = tk.Text(
    editor_frame,
    font=("Segoe UI", 12),
    bg=LIGHT_WHITE,
    fg=LIGHT_TEXT,
    relief="flat",
    wrap="word",
    undo=True,
    insertbackground=LIGHT_TEXT
)

text_box.pack(
    fill="both",
    expand=True
)

text_box.bind(
    "<KeyRelease>",
    update_counter
)


# =========================
# COUNTER
# =========================

counter_label = tk.Label(
    editor_frame,
    text="Words: 0    Characters: 0",
    font=("Segoe UI", 9),
    bg=LIGHT_BG,
    fg="#6B7280"
)

counter_label.pack(
    anchor="e",
    pady=(5, 5)
)


# =========================
# ACTION BUTTONS
# =========================

button_frame = tk.Frame(
    editor_frame,
    bg=LIGHT_BG
)

button_frame.pack(
    fill="x"
)


save_button = tk.Button(
    button_frame,
    text="💾 Save",
    command=save_note,
    bg=LIGHT_BUTTON,
    fg="white",
    relief="flat",
    padx=20,
    pady=8
)

save_button.pack(
    side="left"
)


delete_button = tk.Button(
    button_frame,
    text="🗑 Delete",
    command=delete_note,
    bg=LIGHT_BUTTON,
    fg="white",
    relief="flat",
    padx=20,
    pady=8
)

delete_button.pack(
    side="left",
    padx=8
)


# =========================
# LOAD EXISTING NOTES
# =========================

load_notes()

refresh_notes_list()


# =========================
# START APP
# =========================

root.mainloop()

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import markdown

NOTES_FILE = "notes.json"

class MarkdownNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Notes")
        self.root.geometry("1100x700")
        self.notes = []
        self.current = None
        self.load_notes()
        self.setup_ui()
        self.apply_theme()

    def load_notes(self):
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                self.notes = json.load(f)
        else:
            self.notes = [{"id": 1, "title": "Welcome", "content": "# Hello Markdown", "tags": []}]
            self.save_notes()

    def save_notes(self):
        with open(NOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, width=250, bg="#2d2d2d")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.new_btn = tk.Button(self.sidebar, text="+ New Note", command=self.new_note)
        self.new_btn.pack(pady=5)
        self.search_entry = tk.Entry(self.sidebar)
        self.search_entry.pack(pady=5, fill=tk.X)
        self.search_entry.bind('<KeyRelease>', self.filter_notes)
        self.listbox = tk.Listbox(self.sidebar, bg="#3c3c3c", fg="white")
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.theme_btn = tk.Button(self.sidebar, text="Toggle Theme", command=self.toggle_theme)
        self.theme_btn.pack(pady=5)

        # Main area
        self.main = tk.Frame(self.root)
        self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.title_entry = tk.Entry(self.main, font=("Arial", 16))
        self.title_entry.pack(fill=tk.X, pady=5)
        self.title_entry.bind('<FocusOut>', self.save_current)

        self.paned = tk.PanedWindow(self.main, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)
        self.editor = tk.Text(self.paned, wrap=tk.WORD, font=("Courier", 12), undo=True)
        self.paned.add(self.editor)
        self.preview_frame = tk.Frame(self.paned, bg="white")
        self.paned.add(self.preview_frame)
        self.preview = tk.Text(self.preview_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11))
        self.preview.pack(fill=tk.BOTH, expand=True)
        self.editor.bind('<KeyRelease>', self.update_preview)

        self.toolbar = tk.Frame(self.main)
        self.toolbar.pack(fill=tk.X)
        self.save_btn = tk.Button(self.toolbar, text="Save", command=self.save_current)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        self.export_btn = tk.Button(self.toolbar, text="Export HTML", command=self.export_html)
        self.export_btn.pack(side=tk.LEFT)

        self.refresh_list()

    def refresh_list(self, filter_text=""):
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            if filter_text.lower() in note['title'].lower():
                self.listbox.insert(tk.END, note['title'])

    def filter_notes(self, event=None):
        self.refresh_list(self.search_entry.get())

    def on_select(self, event):
        sel = self.listbox.curselection()
        if sel:
            title = self.listbox.get(sel[0])
            for note in self.notes:
                if note['title'] == title:
                    self.current = note
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, note['title'])
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(1.0, note['content'])
                    self.update_preview()
                    break

    def new_note(self):
        self.current = {"id": max([n['id'] for n in self.notes], default=0)+1, "title": "Untitled", "content": "", "tags": []}
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, "Untitled")
        self.editor.delete(1.0, tk.END)
        self.update_preview()

    def save_current(self, event=None):
        if not self.current:
            return
        self.current['title'] = self.title_entry.get()
        self.current['content'] = self.editor.get(1.0, tk.END).rstrip()
        if self.current['id'] not in [n['id'] for n in self.notes]:
            self.notes.append(self.current)
        else:
            for i, n in enumerate(self.notes):
                if n['id'] == self.current['id']:
                    self.notes[i] = self.current
        self.save_notes()
        self.refresh_list(self.search_entry.get())

    def update_preview(self, event=None):
        md = self.editor.get(1.0, tk.END)
        html = markdown.markdown(md)
        self.preview.config(state=tk.NORMAL)
        self.preview.delete(1.0, tk.END)
        self.preview.insert(tk.END, html)
        self.preview.config(state=tk.DISABLED)

    def export_html(self):
        if not self.current:
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")])
        if filepath:
            html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>{self.current['title']}</title></head><body>{markdown.markdown(self.current['content'])}</body></html>"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            messagebox.showinfo("Exported", f"Saved to {filepath}")

    def toggle_theme(self):
        # Simplified – just switch bg colors
        bg = "#1e1e1e" if self.sidebar.cget("bg") == "#2d2d2d" else "#2d2d2d"
        fg = "white" if bg == "#1e1e1e" else "black"
        self.sidebar.config(bg=bg)
        self.main.config(bg=bg)
        self.editor.config(bg=bg, fg=fg)
        self.preview.config(bg=bg, fg=fg)
        self.title_entry.config(bg=bg, fg=fg)

    def apply_theme(self):
        self.toggle_theme()  # initial dark

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownNotes(root)
    root.mainloop()

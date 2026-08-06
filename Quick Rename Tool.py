import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Get time
def get_file_ctime(filepath):
    stat = os.stat(filepath)
    try:
        return stat.st_birthtime
    except AttributeError:
        return os.path.getctime(filepath)


class BatchRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Rename Tool")
        self.root.geometry("860x600")

        self.folder_path = tk.StringVar()
        self.file_list = []

        self.rename_mode = tk.StringVar(value="add")
        self.add_pos = tk.StringVar(value="suffix")
        self.add_text = tk.StringVar()
        self.sort_by = tk.StringVar(value="time")
        self.reverse_sort = tk.BooleanVar(value=True)

        self.ext_options = ['.txt', '.png', '.jpg', '.docx', '.exe']
        self.ext_vars = {}
        for ext in self.ext_options:
            self.ext_vars[ext] = tk.BooleanVar(value=False)
        self.custom_ext = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        left = ttk.Frame(self.root, width=380)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)
        right = ttk.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=8)

        folder_box = ttk.LabelFrame(left, text="Select Folder", padding=6)
        folder_box.pack(fill=tk.X, pady=5)
        ttk.Button(folder_box, text="Browse", command=self.choose_folder).pack(side=tk.LEFT, padx=2)
        ttk.Entry(folder_box, textvariable=self.folder_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        filter_box = ttk.LabelFrame(left, text="File Extension Filter", padding=6)
        filter_box.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(filter_box, text="txt", variable=self.ext_vars['.txt'], command=self.refresh_list).grid(row=0, column=0, sticky='w', padx=3)
        ttk.Checkbutton(filter_box, text="png", variable=self.ext_vars['.png'], command=self.refresh_list).grid(row=0, column=1, sticky='w', padx=3)
        ttk.Checkbutton(filter_box, text="jpg", variable=self.ext_vars['.jpg'], command=self.refresh_list).grid(row=0, column=2, sticky='w', padx=3)
        ttk.Checkbutton(filter_box, text="docx", variable=self.ext_vars['.docx'], command=self.refresh_list).grid(row=1, column=0, sticky='w', padx=3)
        ttk.Checkbutton(filter_box, text="exe", variable=self.ext_vars['.exe'], command=self.refresh_list).grid(row=1, column=1, sticky='w', padx=3)

        ttk.Label(filter_box, text="Custom:").grid(row=2, column=0, sticky='w')
        ttk.Entry(filter_box, textvariable=self.custom_ext, width=10).grid(row=2, column=1)
        ttk.Button(filter_box, text="Add", command=self.add_ext).grid(row=2, column=2)
        ttk.Label(filter_box, text="No selection = all files", foreground='gray').grid(row=3, column=0, columnspan=3, sticky='w', pady=2)

        mode_box = ttk.LabelFrame(left, text="Rename Mode", padding=6)
        mode_box.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(mode_box, text="Add Prefix/Suffix", variable=self.rename_mode, value="add", command=self.switch_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_box, text="Number Sequence", variable=self.rename_mode, value="number", command=self.switch_mode).pack(side=tk.LEFT, padx=5)

        self.add_panel = ttk.LabelFrame(left, text="Prefix / Suffix Settings", padding=6)
        self.number_panel = ttk.LabelFrame(left, text="Numbering Settings", padding=6)

        ttk.Radiobutton(self.add_panel, text="Add to start (prefix)", variable=self.add_pos, value="prefix").pack(anchor='w', padx=5)
        ttk.Radiobutton(self.add_panel, text="Add after name (suffix)", variable=self.add_pos, value="suffix").pack(anchor='w', padx=5)
        ttk.Entry(self.add_panel, textvariable=self.add_text).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.add_panel, text="Preview Rename", command=self.preview_add).pack(pady=3)

        ttk.Label(self.number_panel, text="Files will become 1.ext, 2.ext ... keep original extension").pack(anchor='w')
        ttk.Radiobutton(self.number_panel, text="Sort by creation time", variable=self.sort_by, value="time").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(self.number_panel, text="Sort by file size", variable=self.sort_by, value="size").pack(anchor='w', padx=5)
        ttk.Checkbutton(self.number_panel, text="Reverse order (newest / largest first)", variable=self.reverse_sort).pack(anchor='w', padx=5, pady=2)
        ttk.Button(self.number_panel, text="Preview Rename", command=self.preview_number).pack(pady=5)

        self.add_panel.pack(fill=tk.X, pady=5)

        ttk.Label(right, text="Files in current folder").pack(anchor='w')
        self.listbox = tk.Listbox(right)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=4)
        scroll = ttk.Scrollbar(self.listbox, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(right, text="Refresh List", command=self.refresh_list).pack(pady=3)

    def switch_mode(self):
        if self.rename_mode.get() == "add":
            self.number_panel.pack_forget()
            self.add_panel.pack(fill=tk.X, pady=5)
        else:
            self.add_panel.pack_forget()
            self.number_panel.pack(fill=tk.X, pady=5)

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)
            self.refresh_list()

    def add_ext(self):
        ext = self.custom_ext.get().strip().lower()
        if not ext:
            return
        if not ext.startswith('.'):
            ext = '.' + ext
        if ext not in self.ext_options:
            self.ext_options.append(ext)
            self.ext_vars[ext] = tk.BooleanVar(value=False)
        self.custom_ext.set("")
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            self.file_list = []
            return

        try:
            all_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read folder: {e}")
            self.file_list = []
            return

        selected = [k for k, v in self.ext_vars.items() if v.get()]
        if selected:
            filtered = []
            for fname in all_files:
                if os.path.splitext(fname)[1].lower() in selected:
                    filtered.append(fname)
            self.file_list = filtered
        else:
            self.file_list = all_files

        for f in self.file_list:
            self.listbox.insert(tk.END, f)

    def show_preview(self, plan):
        win = tk.Toplevel(self.root)
        win.title("Rename Preview")
        win.geometry("600x400")
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="⚠ Backup your files before renaming!", fg='red').pack(pady=5)

        tree = ttk.Treeview(win, columns=("old", "new"), show="headings")
        tree.heading("old", text="Original Name")
        tree.heading("new", text="New Name")
        tree.column("old", width=260)
        tree.column("new", width=260)
        tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        conflict = 0
        folder = self.folder_path.get()
        for old, new in plan:
            new_path = os.path.join(folder, new)
            if os.path.exists(new_path) and old != new:
                tag = "red"
                conflict += 1
            else:
                tag = ""
            tree.insert("", tk.END, values=(old, new), tags=(tag,))
        tree.tag_configure("red", background="#ffcccc")

        if conflict > 0:
            tk.Label(win, text=f"{conflict} filename conflict(s), these will be skipped", fg='darkred').pack()

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Cancel", command=win.destroy).grid(row=0, column=0, padx=10)

        def run_rename():
            self.do_rename(plan)
            win.destroy()
        ttk.Button(btn_frame, text="Execute Rename", command=run_rename).grid(row=0, column=1, padx=10)

    def preview_add(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Warning", "Select a folder first")
            return
        text = self.add_text.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Enter text to insert")
            return
        if not self.file_list:
            messagebox.showinfo("Info", "No matching files")
            return

        plan = []
        pos = self.add_pos.get()
        for old_name in self.file_list:
            name, ext = os.path.splitext(old_name)
            if pos == "prefix":
                new_name = text + name + ext
            else:
                new_name = name + text + ext
            plan.append((old_name, new_name))

        self.show_preview(plan)

    def preview_number(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Warning", "Select a folder first")
            return
        if not self.file_list:
            messagebox.showinfo("Info", "No matching files")
            return

        file_info = []
        for f in self.file_list:
            full_path = os.path.join(folder, f)
            if self.sort_by.get() == "time":
                val = get_file_ctime(full_path)
            else:
                val = os.path.getsize(full_path)
            file_info.append((val, f))

        file_info.sort(key=lambda x: x[0], reverse=self.reverse_sort.get())
        sorted_files = [n for _, n in file_info]

        plan = []
        for i, old_name in enumerate(sorted_files, 1):
            ext = os.path.splitext(old_name)[1]
            plan.append((old_name, f"{i}{ext}"))

        self.show_preview(plan)

    def do_rename(self, plan):
        folder = self.folder_path.get()
        success = 0
        skip = 0
        err = 0

        for old, new in plan:
            old_p = os.path.join(folder, old)
            new_p = os.path.join(folder, new)
            if os.path.exists(new_p) and old_p != new_p:
                skip += 1
                continue
            try:
                os.rename(old_p, new_p)
                success += 1
            except Exception as e:
                err += 1
                print(f"Rename failed: {old} -> {new}, reason: {e}")

        messagebox.showinfo("Completed", f"Success: {success}\nSkipped(conflict): {skip}\nFailed: {err}")
        self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = BatchRenamer(root)
    root.mainloop()

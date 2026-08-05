import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel
from datetime import datetime

def get_file_creation_time(filepath):
    """Get the real creation time of a file across platforms"""
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        ctime = wintypes.FILETIME()
        handle = kernel32.CreateFileW(filepath, 0, 0, None, 3, 0x02000000, None)
        if handle == wintypes.HANDLE(-1).value:
            return os.path.getmtime(filepath)
        kernel32.GetFileTime(handle, ctypes.byref(ctime), None, None)
        kernel32.CloseHandle(handle)
        val = (ctime.dwHighDateTime << 32) + ctime.dwLowDateTime
        return (val / 10000000) - 11644473600
    else:
        stat = os.stat(filepath)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


class BatchRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch File Renamer (Safe Preview)")
        self.root.geometry("880x620")
        self.root.resizable(True, True)

        # 变量
        self.folder_path = tk.StringVar()
        self.mode = tk.StringVar(value="add")  # add / number
        self.add_position = tk.StringVar(value="suffix")  # prefix / suffix
        self.add_text = tk.StringVar()
        self.number_criteria = tk.StringVar(value="time")  # time / size
        self.number_reverse_sort = tk.BooleanVar(value=True)
        self.file_list = []

        self.extensions = ['.txt', '.png', '.jpg', '.docx', '.exe']
        self.ext_vars = {ext: tk.BooleanVar(value=False) for ext in self.extensions}
        self.custom_ext = tk.StringVar()

        self.create_widgets()
        self.update_mode_ui()

    def create_widgets(self):
        main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.Frame(main_panel, width=400)
        main_panel.add(left_frame, weight=1)

        folder_frame = ttk.LabelFrame(left_frame, text="Folder Selection", padding=5)
        folder_frame.pack(fill=tk.X, pady=5)
        ttk.Button(folder_frame, text="Browse Folder", command=self.select_folder).pack(side=tk.LEFT, padx=2)
        ttk.Entry(folder_frame, textvariable=self.folder_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        filter_frame = ttk.LabelFrame(left_frame, text="Extension Filter", padding=5)
        filter_frame.pack(fill=tk.X, pady=5)
        row, col = 0, 0
        for ext in self.extensions:
            disp = ext.lstrip('.')
            chk = ttk.Checkbutton(filter_frame, text=disp, variable=self.ext_vars[ext],
                                  command=self.refresh_file_list)
            chk.grid(row=row, column=col, sticky=tk.W, padx=3, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1
        ttk.Label(filter_frame, text="Custom:", foreground="gray").grid(row=row+1, column=0, sticky=tk.W)
        ttk.Entry(filter_frame, textvariable=self.custom_ext, width=10).grid(row=row+1, column=1)
        ttk.Button(filter_frame, text="Add", command=self.add_custom_ext).grid(row=row+1, column=2)
        ttk.Label(filter_frame, text="(None=all files)", foreground="gray").grid(row=row+2, column=0, columnspan=3, sticky=tk.W)

        mode_frame = ttk.LabelFrame(left_frame, text="Mode", padding=5)
        mode_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(mode_frame, text="Add Suffix/Prefix", variable=self.mode, value="add", command=self.update_mode_ui).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(mode_frame, text="Number Sequence", variable=self.mode, value="number", command=self.update_mode_ui).pack(side=tk.LEFT, padx=4)

        self.dynamic_frame = ttk.Frame(left_frame)
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        right_frame = ttk.Frame(main_panel)
        main_panel.add(right_frame, weight=2)
        ttk.Label(right_frame, text="Files in Folder (filtered)").pack(anchor=tk.W)
        self.file_listbox = tk.Listbox(right_frame)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=4)
        scrollbar = ttk.Scrollbar(self.file_listbox, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(right_frame, text="Refresh List", command=self.refresh_file_list).pack(pady=2)

    def add_custom_ext(self):
        txt = self.custom_ext.get().strip().lower()
        if not txt:
            return
        if not txt.startswith('.'):
            txt = '.' + txt
        if txt not in self.extensions:
            self.extensions.append(txt)
            self.ext_vars[txt] = tk.BooleanVar(value=False)
        self.custom_ext.set("")
        self.refresh_file_list()

    def update_mode_ui(self):
        for child in self.dynamic_frame.winfo_children():
            child.destroy()
        if self.mode.get() == "add":
            self.create_add_mode_ui()
        else:
            self.create_number_mode_ui()

    def create_add_mode_ui(self):
        frame = ttk.Frame(self.dynamic_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        pos_frame = ttk.LabelFrame(frame, text="Position", padding=5)
        pos_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(pos_frame, text="Prefix (start)", variable=self.add_position, value="prefix").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(pos_frame, text="Suffix (end before ext)", variable=self.add_position, value="suffix").pack(side=tk.LEFT, padx=5)

        entry_frame = ttk.LabelFrame(frame, text="Text to Insert", padding=5)
        entry_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(entry_frame, textvariable=self.add_text).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(entry_frame, text="Preview Rename", command=self.preview_add_mode).pack(side=tk.LEFT, padx=4)
        ttk.Label(frame, text="Example: file.txt → PREFIXfile.txt / fileSUFFIX.txt", foreground="gray").pack(pady=4)

    def create_number_mode_ui(self):
        frame = ttk.Frame(self.dynamic_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        info = ttk.LabelFrame(frame, text="Info", padding=5)
        info.pack(fill=tk.X, pady=5)
        ttk.Label(info, text="Rename files to 1.ext, 2.ext … keep original extension.", wraplength=320).pack(anchor=tk.W)

        criteria_frame = ttk.LabelFrame(frame, text="Sort files by", padding=5)
        criteria_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(criteria_frame, text="File Create Time", variable=self.number_criteria, value="time").pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(criteria_frame, text="File Size", variable=self.number_criteria, value="size").pack(side=tk.LEFT, padx=4)

        order_frame = ttk.LabelFrame(frame, text="Sort Direction", padding=5)
        order_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(order_frame, text="Reverse (Newest / Largest first)", variable=self.number_reverse_sort).pack(anchor=tk.W)
        ttk.Button(frame, text="Preview Number Rename", command=self.preview_number_mode).pack(pady=10)

    def select_folder(self):
        fd = filedialog.askdirectory()
        if fd:
            self.folder_path.set(fd)
            self.refresh_file_list()

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        fp = self.folder_path.get()
        if not fp or not os.path.isdir(fp):
            self.file_list = []
            return
        try:
            all_entries = os.listdir(fp)
            files = [f for f in all_entries if os.path.isfile(os.path.join(fp, f))]
        except Exception as e:
            messagebox.showerror("Folder Error", str(e))
            self.file_list = []
            return

        selected_exts = [k for k, v in self.ext_vars.items() if v.get()]
        if selected_exts:
            filtered = []
            for fname in files:
                _, e = os.path.splitext(fname)
                if e.lower() in [x.lower() for x in selected_exts]:
                    filtered.append(fname)
        else:
            filtered = files
        self.file_list = filtered
        for f in filtered:
            self.file_listbox.insert(tk.END, f)

    def show_preview_window(self, rename_plan):
        """rename_plan: list[(old_name, new_name)]"""
        win = Toplevel(self.root)
        win.title("Rename Preview — Confirm before apply!")
        win.geometry("640x420")
        ttk.Label(win, text="⚠️ Please backup files before executing rename!", foreground="red").pack(pady=3)
        frame = ttk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        tree = ttk.Treeview(frame, columns=("old", "new"), show="headings")
        tree.heading("old", text="Original Name")
        tree.heading("new", text="Will become")
        tree.column("old", width=280)
        tree.column("new", width=280)
        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        conflict_count = 0
        folder = self.folder_path.get()
        for old, new in rename_plan:
            full_new = os.path.join(folder, new)
            conflict = os.path.exists(full_new)
            tag = "conflict" if conflict else ""
            if conflict:
                conflict_count +=1
            tree.insert("", tk.END, values=(old, new), tags=(tag,))
        tree.tag_configure("conflict", background="#ffcccc")

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=6)
        ttk.Button(btn_frame, text="Cancel", command=win.destroy).grid(row=0, column=0, padx=8)
        def do_execute():
            self.execute_rename(rename_plan)
            win.destroy()
        if conflict_count>0:
            ttk.Label(btn_frame, text=f"{conflict_count} filename conflicts (red rows), will skip them", foreground="darkred").grid(row=1,column=0,columnspan=2)
        ttk.Button(btn_frame, text="Execute Rename", command=do_execute).grid(row=0, column=1, padx=8)
        win.transient(self.root)
        win.grab_set()

    def preview_add_mode(self):
        fp = self.folder_path.get()
        if not fp or not os.path.isdir(fp):
            messagebox.showwarning("Warning", "Select folder first")
            return
        text = self.add_text.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Fill text to add")
            return
        files = self.file_list
        if not files:
            messagebox.showinfo("Info", "No filtered files")
            return
        pos = self.add_position.get()
        plan = []
        for old in files:
            name, ext = os.path.splitext(old)
            if pos == "prefix":
                new = text + name + ext
            else:
                new = name + text + ext
            plan.append((old, new))
        self.show_preview_window(plan)

    def preview_number_mode(self):
        fp = self.folder_path.get()
        if not fp or not os.path.isdir(fp):
            messagebox.showwarning("Warning", "Select folder first")
            return
        files = self.file_list
        if not files:
            messagebox.showinfo("Info", "No filtered files")
            return
        crit = self.number_criteria.get()
        rev = self.number_reverse_sort.get()
        finfo = []
        for f in files:
            full = os.path.join(fp, f)
            if crit == "time":
                tm = get_file_creation_time(full)
                finfo.append((tm, f))
            else:
                sz = os.path.getsize(full)
                finfo.append((sz, f))
        finfo.sort(key=lambda x:x[0], reverse=rev)
        sorted_names = [n for _,n in finfo]
        plan = []
        for idx, old in enumerate(sorted_names, start=1):
            _, ext = os.path.splitext(old)
            new = f"{idx}{ext}"
            plan.append((old, new))
        self.show_preview_window(plan)

    def execute_rename(self, rename_plan):
        folder = self.folder_path.get()
        ok = 0
        skip_conflict = 0
        error = 0
        for old_name, new_name in rename_plan:
            oldp = os.path.join(folder, old_name)
            newp = os.path.join(folder, new_name)
            if os.path.exists(newp) and oldp != newp:
                skip_conflict += 1
                continue
            try:
                os.rename(oldp, newp)
                ok += 1
            except Exception as e:
                error +=1
                messagebox.showerror("Rename Error", f"{old_name} → {new_name}\n{e}")
        messagebox.showinfo("Complete",
                            f"Success:{ok}\nSkipped(conflict):{skip_conflict}\nErrors:{error}")
        self.refresh_file_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = BatchRenamerApp(root)
    root.mainloop()

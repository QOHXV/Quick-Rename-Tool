import sys
import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
#语言
STRINGS = {
    "en": {
        "app_title": "File Organizer",
        "tab_rename": "Rename",
        "tab_photo": "Photo Filter",
        "select_folder": "Select Folder",
        "no_folder": "No folder selected",
        "mode_add": "Add Name Mode",
        "mode_num": "Number Order Mode",
        "add_title": "Add Name Mode",
        "add_hint": "Add text to the beginning or end of every file name.",
        "position": "Position",
        "prefix": "Beginning",
        "suffix": "End",
        "content": "Content",
        "add": "Add",
        "num_title": "Number Order Mode",
        "num_desc": "After clicking Start, files are renamed as 1, 2, 3...\nChoose the reference used for ordering.",
        "sort_by": "Sort by",
        "by_ctime": "Creation Time",
        "by_size": "File Size",
        "order": "Order",
        "new_to_old": "Newest → Oldest",
        "old_to_new": "Oldest → Newest",
        "small_to_large": "Smallest → Largest",
        "large_to_small": "Largest → Smallest",
        "start_sort": "Start Renaming",
        "col_i": "#", "col_name": "File Name",
        "col_size": "Size", "col_created": "Created",
        "size_label": "File size (MB)",
        "ext_label": "Extensions",
        "time_label": "Date range",
        "filter": "Filter",
        "reset": "Reset",
        "rename_label": "Rename",
        "rename_selected": "Rename Selected",
        "copy": "Copy", "cut": "Cut", "delete": "Delete",
        "warn_title": "Subfolders Detected",
        "warn_sub": "The selected folder contains subfolders.\nPlease choose a folder that contains only files.",
        "notice": "Notice",
        "need_folder": "Please select a folder first.",
        "need_content": "Please enter the content to add.",
        "need_selection": "Please select at least one file.",
        "done_add": "Renamed {n} file(s).",
        "done_number": "Renamed {n} file(s) as 1, 2, 3...",
        "done_filter": "Found {n} matching file(s).",
        "confirm_title": "Confirm",
        "confirm_delete": "Delete {n} selected file(s)? This cannot be undone.",
        "copied": "Copied {n} file(s).",
        "moved": "Moved {n} file(s).",
        "deleted": "Deleted {n} file(s).",
        "bad_number": "Invalid number: {v}",
        "bad_date": "Invalid date: {v}",
        "no_match": "No file matches the current filter.",
        "files_count": "{n} file(s)",
        "language": "Language"
    },
    "zh": {
        "app_title": "文件整理工具",
        "tab_rename": "重命名",
        "tab_photo": "照片筛选",
        "select_folder": "选择文件夹",
        "no_folder": "未选择文件夹",
        "mode_add": "添加名称模式",
        "mode_num": "数字排列模式",
        "add_title": "添加名称模式",
        "add_hint": "在每个文件名的开头或结尾添加内容。",
        "position": "位置",
        "prefix": "开头",
        "suffix": "结尾",
        "content": "内容",
        "add": "添加",
        "num_title": "数字排列模式",
        "num_desc": "点击开始后，软件会自动将文件按照 1、2、3…… 排列好，\n您可以选择排列的参考指标。",
        "sort_by": "参考指标",
        "by_ctime": "创建时间",
        "by_size": "文件大小",
        "order": "排列顺序",
        "new_to_old": "从新到旧",
        "old_to_new": "从旧到新",
        "small_to_large": "小到大",
        "large_to_small": "大到小",
        "start_sort": "开始排列",
        "col_i": "序号", "col_name": "文件名",
        "col_size": "大小", "col_created": "创建时间",
        "size_label": "文件大小（MB）",
        "ext_label": "后缀名",
        "time_label": "时间范围",
        "filter": "筛选",
        "reset": "重置",
        "rename_label": "重命名",
        "rename_selected": "重命名所选",
        "copy": "复制", "cut": "剪切", "delete": "删除",
        "warn_title": "检测到子文件夹",
        "warn_sub": "所选文件夹内含有子文件夹。\n请选择一个只包含文件的文件夹。",
        "notice": "提示",
        "need_folder": "请先选择文件夹。",
        "need_content": "请输入要添加的内容。",
        "need_selection": "请至少选择一个文件。",
        "done_add": "已重命名 {n} 个文件。",
        "done_number": "已将 {n} 个文件按 1、2、3…… 排列。",
        "done_filter": "找到 {n} 个匹配文件。",
        "confirm_title": "确认",
        "confirm_delete": "确定删除选中的 {n} 个文件吗？此操作不可撤销。",
        "copied": "已复制 {n} 个文件。",
        "moved": "已剪切 {n} 个文件。",
        "deleted": "已删除 {n} 个文件。",
        "bad_number": "无效的数字：{v}",
        "bad_date": "无效的日期：{v}",
        "no_match": "没有文件符合当前筛选条件。",
        "files_count": "{n} 个文件",
        "language": "语言"
    }
}


# 工具函数
def human_size(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"

def fmt_time(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

def split_name(name):
    idx = name.rfind(".")
    if idx <= 0:
        return name, ""
    return name[:idx], name[idx:]
    #程序
class FileOrganizerTk:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.folder = None
        self.files = []
        self.photo_files = []

        # 变量
        self.var_mode_add = tk.BooleanVar(value=True)
        self.var_pos = tk.StringVar()
        self.var_pos2 = tk.StringVar()
        self.var_sort = tk.StringVar()
        self.var_order = tk.StringVar()

        self.var_jpg = tk.BooleanVar(value=True)
        self.var_png = tk.BooleanVar(value=True)
        self.var_nef = tk.BooleanVar(value=True)
        self.var_hif = tk.BooleanVar(value=True)

        self.build_ui()
        self.apply_language()

    def t(self, key: str) -> str:
        lang_strings = STRINGS.get(self.lang)
        if lang_strings is None:
            return key
        value = lang_strings.get(key, key)
        return value if value is not None else key

    def build_ui(self):
        self.root.minsize(1180, 720)
        self.root.title(self.t("app_title"))

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 顶部栏
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0,12))
        self.title_label = ttk.Label(top_frame, font=("Microsoft YaHei",16,"bold"))
        self.title_label.pack(side=tk.LEFT)
        ttk.Label(top_frame, text=" ").pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.lang_label = ttk.Label(top_frame)
        self.lang_label.pack(side=tk.LEFT)
        self.lang_combo = ttk.Combobox(top_frame, values=["English", "中文"], state="readonly", width=10)
        self.lang_combo.current(0)
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_lang_change)
        self.lang_combo.pack(side=tk.LEFT, padx=5)

        # 标签页
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_rename = ttk.Frame(self.notebook)
        self.tab_photo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rename)
        self.notebook.add(self.tab_photo)

        self.build_rename_tab()
        self.build_photo_tab()
        
    def build_rename_tab(self):
        page = self.tab_rename
        # 文件夹选择
        folder_frame = ttk.Frame(page)
        folder_frame.pack(fill=tk.X, pady=(0,10))
        self.btn_pick1 = ttk.Button(folder_frame, command=self.pick_folder)
        self.btn_pick1.pack(side=tk.LEFT)
        self.path_label1 = ttk.Label(folder_frame)
        self.path_label1.pack(side=tk.LEFT, padx=10)

        body_frame = ttk.Frame(page)
        body_frame.pack(fill=tk.BOTH, expand=True)
        left_panel = ttk.Frame(body_frame, width=340)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        right_panel = ttk.Frame(body_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 按钮
        mode_frame = ttk.Frame(left_panel)
        mode_frame.pack(fill=tk.X, pady=(0,10))
        self.btn_mode_add = ttk.Radiobutton(mode_frame, variable=self.var_mode_add, value=True, command=lambda:self.switch_mode("add"))
        self.btn_mode_num = ttk.Radiobutton(mode_frame, variable=self.var_mode_add, value=False, command=lambda:self.switch_mode("number"))
        self.btn_mode_add.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_mode_num.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # add name
        self.group_add = ttk.LabelFrame(left_panel)
        ga = ttk.Frame(self.group_add, padding=10)
        ga.pack(fill=tk.BOTH)
        self.lbl_pos = ttk.Label(ga)
        self.pos_combo = ttk.Combobox(ga, textvariable=self.var_pos, state="readonly")
        self.lbl_content = ttk.Label(ga)
        self.content_input = ttk.Entry(ga)
        self.btn_add = ttk.Button(ga, command=self.do_add_name)
        self.lbl_pos.pack(anchor="w")
        self.pos_combo.pack(fill=tk.X, pady=3)
        self.lbl_content.pack(anchor="w")
        self.content_input.pack(fill=tk.X, pady=3)
        self.btn_add.pack(pady=5)
        self.group_add.pack(fill=tk.X, pady=5)

        # mumber分组
        self.group_num = ttk.LabelFrame(left_panel)
        gn = ttk.Frame(self.group_num, padding=10)
        gn.pack(fill=tk.BOTH)
        self.lbl_num_desc = ttk.Label(gn, wraplength=300)
        self.lbl_sort = ttk.Label(gn)
        self.sort_combo = ttk.Combobox(gn, textvariable=self.var_sort, state="readonly")
        self.lbl_order = ttk.Label(gn)
        self.order_combo = ttk.Combobox(gn, textvariable=self.var_order, state="readonly")
        self.btn_start_sort = ttk.Button(gn, command=self.do_number_order)
        self.lbl_num_desc.pack(anchor="w")
        self.lbl_sort.pack(anchor="w")
        self.sort_combo.pack(fill=tk.X, pady=3)
        self.lbl_order.pack(anchor="w")
        self.order_combo.pack(fill=tk.X, pady=3)
        self.btn_start_sort.pack(pady=5)

        # 文件列表
        self.count_label1 = ttk.Label(right_panel)
        self.count_label1.pack(anchor="w")
        self.table1 = ttk.Treeview(right_panel, columns=("col1","col2","col3","col4"), show="headings")
        self.table1.heading("col1", text="#")
        self.table1.heading("col2", text="FileName")
        self.table1.heading("col3", text="Size")
        self.table1.heading("col4", text="Created")
        self.table1.column("col1", width=50)
        self.table1.column("col2", width=250)
        self.table1.column("col3", width=120)
        self.table1.column("col4", width=180)
        scroll1 = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.table1.yview)
        self.table1.configure(yscrollcommand=scroll1.set)
        self.table1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)

    #筛选
    def build_photo_tab(self):
        page = self.tab_photo
        folder_frame = ttk.Frame(page)
        folder_frame.pack(fill=tk.X, pady=(0,10))
        self.btn_pick2 = ttk.Button(folder_frame, command=self.pick_folder)
        self.btn_pick2.pack(side=tk.LEFT)
        self.path_label2 = ttk.Label(folder_frame)
        self.path_label2.pack(side=tk.LEFT, padx=10)

        filter_box = ttk.LabelFrame(page)
        filter_box.pack(fill=tk.X, pady=5)
        fb = ttk.Frame(filter_box, padding=10)
        fb.pack(fill=tk.X)

        # 大小
        size_row = ttk.Frame(fb)
        size_row.pack(fill=tk.X)
        self.lbl_size = ttk.Label(size_row)
        self.size_min = ttk.Entry(size_row, width=8)
        self.size_min.insert(0,"0")
        self.size_max = ttk.Entry(size_row, width=8)
        self.size_max.insert(0,"5")
        ttk.Label(size_row, text=" – ").pack(side=tk.LEFT)
        self.lbl_mb = ttk.Label(size_row, text="MB")
        self.lbl_size.pack(side=tk.LEFT)
        self.size_min.pack(side=tk.LEFT)
        self.size_max.pack(side=tk.LEFT)
        self.lbl_mb.pack(side=tk.LEFT)

        # 后缀
        ext_row = ttk.Frame(fb)
        ext_row.pack(fill=tk.X)
        self.lbl_ext = ttk.Label(ext_row)
        chk_jpg = ttk.Checkbutton(ext_row, text="jpg", variable=self.var_jpg)
        chk_png = ttk.Checkbutton(ext_row, text="png", variable=self.var_png)
        chk_nef = ttk.Checkbutton(ext_row, text="NEF", variable=self.var_nef)
        chk_hif = ttk.Checkbutton(ext_row, text="HIF", variable=self.var_hif)
        self.lbl_ext.pack(side=tk.LEFT)
        chk_jpg.pack(side=tk.LEFT)
        chk_png.pack(side=tk.LEFT)
        chk_nef.pack(side=tk.LEFT)
        chk_hif.pack(side=tk.LEFT)

        # 时间
        time_row = ttk.Frame(fb)
        time_row.pack(fill=tk.X)
        self.lbl_time = ttk.Label(time_row)
        self.date_from = ttk.Entry(time_row)
        self.date_to = ttk.Entry(time_row)
        self.date_from.insert(0,"2024-01-01")
        self.date_to.insert(0,"2024-12-31")
        self.lbl_time.pack(side=tk.LEFT)
        self.date_from.pack(side=tk.LEFT)
        ttk.Label(time_row, text=" – ").pack(side=tk.LEFT)
        self.date_to.pack(side=tk.LEFT)

        # 筛选按钮
        btn_row = ttk.Frame(fb)
        btn_row.pack(fill=tk.X)
        self.btn_filter = ttk.Button(btn_row, command=self.do_filter)
        self.btn_reset = ttk.Button(btn_row, command=self.reset_filter)
        self.btn_filter.pack(side=tk.LEFT)
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        # 结果表格
        self.count_label2 = ttk.Label(page)
        self.count_label2.pack(anchor="w")
        self.table2 = ttk.Treeview(page, columns=("col1","col2","col3","col4"), show="headings")
        self.table2.heading("col1", text="#")
        self.table2.heading("col2", text="FileName")
        self.table2.heading("col3", text="Size")
        self.table2.heading("col4", text="Created")
        self.table2.column("col1", width=50)
        self.table2.column("col2", width=250)
        self.table2.column("col3", width=120)
        self.table2.column("col4", width=180)
        scroll2 = ttk.Scrollbar(page, orient=tk.VERTICAL, command=self.table2.yview)
        self.table2.configure(yscrollcommand=scroll2.set)
        self.table2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll2.pack(side=tk.RIGHT, fill=tk.Y)

        # 操作栏
        action_bar = ttk.Frame(page)
        action_bar.pack(fill=tk.X, pady=5)
        self.lbl_rename = ttk.Label(action_bar)
        self.pos_combo2 = ttk.Combobox(action_bar, textvariable=self.var_pos2, state="readonly")
        self.content_input2 = ttk.Entry(action_bar)
        self.btn_rename_sel = ttk.Button(action_bar, command=self.photo_rename)
        self.btn_copy = ttk.Button(action_bar, command=lambda:self.photo_transfer(cut=False))
        self.btn_cut = ttk.Button(action_bar, command=lambda:self.photo_transfer(cut=True))
        self.btn_delete = ttk.Button(action_bar, command=self.photo_delete)
        self.lbl_rename.pack(side=tk.LEFT)
        self.pos_combo2.pack(side=tk.LEFT)
        self.content_input2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_rename_sel.pack(side=tk.LEFT)
        self.btn_copy.pack(side=tk.LEFT)
        self.btn_cut.pack(side=tk.LEFT)
        self.btn_delete.pack(side=tk.LEFT)
        
    def on_lang_change(self, event):
        self.lang = "zh" if self.lang_combo.current() == 1 else "en"
        self.apply_language()

    def apply_language(self):
        s = STRINGS[self.lang]
        self.root.title(s["app_title"])
        self.title_label.config(text=s["app_title"])
        self.lang_label.config(text=s["language"])
        self.notebook.tab(self.tab_rename, text=s["tab_rename"])
        self.notebook.tab(self.tab_photo, text=s["tab_photo"])
        self.btn_pick1.config(text=s["select_folder"])
        self.btn_pick2.config(text=s["select_folder"])
        self.path_label1.config(text=self.folder or s["no_folder"])
        self.path_label2.config(text=self.folder or s["no_folder"])
        self.btn_mode_add.config(text=s["mode_add"])
        self.btn_mode_num.config(text=s["mode_num"])
        self.group_add.config(text=s["add_title"])
        self.lbl_pos.config(text=s["position"])
        self.lbl_content.config(text=s["content"])
        self.btn_add.config(text=s["add"])
        self.group_num.config(text=s["num_title"])
        self.lbl_num_desc.config(text=s["num_desc"])
        self.lbl_sort.config(text=s["sort_by"])
        self.lbl_order.config(text=s["order"])
        self.btn_start_sort.config(text=s["start_sort"])
        self._fill_pos_combo(self.pos_combo)
        self._fill_pos_combo(self.pos_combo2)
        self._fill_sort_combo()
        self._fill_order_combo()
        self.table1.heading("col1", text=s["col_i"])
        self.table1.heading("col2", text=s["col_name"])
        self.table1.heading("col3", text=s["col_size"])
        self.table1.heading("col4", text=s["col_created"])
        self.table2.heading("col1", text=s["col_i"])
        self.table2.heading("col2", text=s["col_name"])
        self.table2.heading("col3", text=s["col_size"])
        self.table2.heading("col4", text=s["col_created"])
        self.lbl_size.config(text=s["size_label"])
        self.lbl_ext.config(text=s["ext_label"])
        self.lbl_time.config(text=s["time_label"])
        self.btn_filter.config(text=s["filter"])
        self.btn_reset.config(text=s["reset"])
        self.lbl_rename.config(text=s["rename_label"])
        self.btn_rename_sel.config(text=s["rename_selected"])
        self.btn_copy.config(text=s["copy"])
        self.btn_cut.config(text=s["cut"])
        self.btn_delete.config(text=s["delete"])
        self.refresh_count_labels()
        self.render_table1()
        self.render_table2()

    def _fill_pos_combo(self, combo):
        old = combo.current()
        combo["values"] = [self.t("prefix"), self.t("suffix")]
        combo.current(max(0, old))

    def _fill_sort_combo(self):
        old = self.sort_combo.current()
        self.sort_combo["values"] = [self.t("by_ctime"), self.t("by_size")]
        self.sort_combo.current(max(0, old))
        self._fill_order_combo()

    def _fill_order_combo(self):
        old = self.order_combo.current()
        if self.sort_combo.current() == 0:
            self.order_combo["values"] = [self.t("new_to_old"), self.t("old_to_new")]
        else:
            self.order_combo["values"] = [self.t("small_to_large"), self.t("large_to_small")]
        self.order_combo.current(max(0, old))

    def switch_mode(self, mode):
        if mode == "add":
            self.group_add.pack(fill=tk.X, pady=5)
            self.group_num.pack_forget()
        else:
            self.group_add.pack_forget()
            self.group_num.pack(fill=tk.X, pady=5)

    #文件夹读取
    def pick_folder(self):
        folder = filedialog.askdirectory(title=self.t("select_folder"))
        if not folder:
            return
        # 检测子文件夹
        for entry in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, entry)):
                messagebox.showwarning(self.t("warn_title"), self.t("warn_sub"))
                return
        self.folder = folder
        self.path_label1.config(text=folder)
        self.path_label2.config(text=folder)
        self.load_files()

    def load_files(self):
        if not self.folder:
            return
        self.files = []
        for name in os.listdir(self.folder):
            path = os.path.join(self.folder, name)
            if not os.path.isfile(path):
                continue
            try:
                st = os.stat(path)
                self.files.append({"name": name, "path": path, "size": st.st_size, "ctime": st.st_ctime})
            except OSError:
                continue
        self.files.sort(key=lambda x:x["name"].lower())
        self.render_table1()

    def render_table1(self):
        self.table1.delete(*self.table1.get_children())
        for i, f in enumerate(self.files):
            self.table1.insert("", tk.END, values=(i+1, f["name"], human_size(f["size"]), fmt_time(f["ctime"])))
        self.refresh_count_labels()

    def render_table2(self):
        self.table2.delete(*self.table2.get_children())
        for i, f in enumerate(self.photo_files):
            self.table2.insert("", tk.END, values=(i+1, f["name"], human_size(f["size"]), fmt_time(f["ctime"])))
        self.refresh_count_labels()

    def refresh_count_labels(self):
        self.count_label1.config(text=self.t("files_count").format(n=len(self.files)))
        self.count_label2.config(text=self.t("files_count").format(n=len(self.photo_files)))
        
    def apply_renames(self, pairs):
        folder = self.folder
        if folder is None:
            return 0
        temp_map = []
        for i, (old, new) in enumerate(pairs):
            old_path = os.path.join(folder, old)
            tmp_name = f".__tmp_{datetime.now().timestamp()}_{i}__"
            tmp_path = os.path.join(folder, tmp_name)
            try:
                os.rename(old_path, tmp_path)
                temp_map.append((tmp_path, new))
            except OSError:
                continue
        ok = 0
        for tmp_path, new_name in temp_map:
            new_path = os.path.join(folder, new_name)
            try:
                os.rename(tmp_path, new_path)
                ok += 1
            except OSError:
                try: os.rename(tmp_path, tmp_path+".restore")
                except: pass
        return ok

    def do_add_name(self):
        if not self.folder:
            messagebox.showinfo(self.t("notice"), self.t("need_folder"))
            return
        content = self.content_input.get().strip()
        if not content:
            messagebox.showinfo(self.t("notice"), self.t("need_content"))
            return
        pos = self.pos_combo.current()
        pairs = []
        for f in self.files:
            base, ext = split_name(f["name"])
            new_name = (content + base + ext) if pos == 0 else (base + content + ext)
            if new_name != f["name"]:
                pairs.append((f["name"], new_name))
        ok = self.apply_renames(pairs)
        self.load_files()
        if ok>0:
            messagebox.showinfo(self.t("notice"), self.t("done_add").format(n=ok))

    def do_number_order(self):
        if not self.folder:
            messagebox.showinfo(self.t("notice"), self.t("need_folder"))
            return
        sort_idx = self.sort_combo.current()
        order_idx = self.order_combo.current()
        items = self.files[:]
        if sort_idx == 0:
            items.sort(key=lambda x:x["ctime"], reverse=(order_idx ==0))
        else:
            items.sort(key=lambda x:x["size"], reverse=(order_idx ==1))
        pairs = []
        for i,f in enumerate(items):
            base, ext = split_name(f["name"])
            new_name = f"{i+1}{ext}"
            if new_name != f["name"]:
                pairs.append((f["name"], new_name))
        ok = self.apply_renames(pairs)
        self.load_files()
        if ok>0:
            messagebox.showinfo(self.t("notice"), self.t("done_number").format(n=ok))

    #照片筛选
    def do_filter(self, silent=False):
        if not self.folder:
            messagebox.showinfo(self.t("notice"), self.t("need_folder"))
            return
        self.load_files()
        try:
            min_mb = float(self.size_min.get().strip()) if self.size_min.get().strip() else None
            max_mb = float(self.size_max.get().strip()) if self.size_max.get().strip() else None
        except ValueError:
            if not silent:
                messagebox.showwarning(self.t("notice"), self.t("bad_number").format(v="size"))
            return
        t0 = self._parse_date(self.date_from.get().strip(), end=False)
        t1 = self._parse_date(self.date_to.get().strip(), end=True)
        if t0 is False or t1 is False:
            return
        checked = []
        if self.var_jpg.get(): checked.append("jpg")
        if self.var_png.get(): checked.append("png")
        if self.var_nef.get(): checked.append("nef")
        if self.var_hif.get(): checked.append("hif")
        result = []
        for f in self.files:
            ext = split_name(f["name"])[1].lower().lstrip(".")
            if checked and ext not in checked:
                continue
            mb = f["size"]/(1024*1024)
            if min_mb is not None and mb < min_mb: continue
            if max_mb is not None and mb > max_mb: continue
            if t0 is not None and f["ctime"] < t0: continue
            if t1 is not None and f["ctime"] > t1: continue
            result.append(f)
        self.photo_files = result
        self.render_table2()
        if not silent:
            messagebox.showinfo(self.t("notice"), self.t("done_filter").format(n=len(result)))

    def _parse_date(self, text, end):
        if not text:
            return None
        try:
            dt = datetime.strptime(text.replace("/","-"), "%Y-%m-%d")
            if end:
                dt = dt.replace(hour=23, minute=59, second=59)
            return dt.timestamp()
        except ValueError:
            messagebox.showwarning(self.t("notice"), self.t("bad_date").format(v=text))
            return False

    def reset_filter(self):
        self.size_min.delete(0, tk.END)
        self.size_min.insert(0,"0")
        self.size_max.delete(0, tk.END)
        self.size_max.insert(0,"5")
        self.date_from.delete(0, tk.END)
        self.date_to.delete(0, tk.END)
        self.var_jpg.set(True)
        self.var_png.set(True)
        self.var_nef.set(True)
        self.var_hif.set(True)
        self.photo_files = []
        self.render_table2()

    def get_selected_photos(self):
        sel = self.table2.selection()
        if not sel:
            return self.photo_files[:]
        rows_idx = [self.table2.index(iid) for iid in sel]
        return [self.photo_files[r] for r in rows_idx if r < len(self.photo_files)]

    def photo_rename(self):
        targets = self.get_selected_photos()
        if not targets:
            messagebox.showinfo(self.t("notice"), self.t("need_selection"))
            return
        content = self.content_input2.get().strip()
        if not content:
            messagebox.showinfo(self.t("notice"), self.t("need_content"))
            return
        pos = self.pos_combo2.current()
        pairs = []
        for f in targets:
            base, ext = split_name(f["name"])
            new_name = (content + base + ext) if pos ==0 else (base + content + ext)
            if new_name != f["name"]:
                pairs.append((f["name"], new_name))
        ok = self.apply_renames(pairs)
        self.do_filter(silent=True)
        if ok>0:
            messagebox.showinfo(self.t("notice"), self.t("done_add").format(n=ok))

    def photo_delete(self):
        targets = self.get_selected_photos()
        if not targets:
            messagebox.showinfo(self.t("notice"), self.t("need_selection"))
            return
        ans = messagebox.askyesno(self.t("confirm_title"), self.t("confirm_delete").format(n=len(targets)))
        if not ans:
            return
        ok = 0
        for f in targets:
            try:
                os.remove(f["path"])
                ok +=1
            except OSError:
                pass
        self.do_filter(silent=True)
        messagebox.showinfo(self.t("notice"), self.t("deleted").format(n=ok))

    def photo_transfer(self, cut):
        targets = self.get_selected_photos()
        if not targets:
            messagebox.showinfo(self.t("notice"), self.t("need_selection"))
            return
        dst = filedialog.askdirectory(title=self.t("select_folder"))
        if not dst:
            return
        ok = 0
        for f in targets:
            try:
                base, ext = split_name(f["name"])
                target_name = f["name"]
                target_path = os.path.join(dst, target_name)
                n=1
                while os.path.exists(target_path):
                    target_name = f"{base}_{n}{ext}"
                    target_path = os.path.join(dst, target_name)
                    n +=1
                if cut:
                    shutil.move(f["path"], target_path)
                else:
                    shutil.copy2(f["path"], target_path)
                ok +=1
            except OSError:
                continue
        self.do_filter(silent=True)
        key = "moved" if cut else "copied"
        messagebox.showinfo(self.t("notice"), self.t(key).format(n=ok))
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerTk(root)
    root.mainloop()

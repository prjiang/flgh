import tkinter as tk
from tkinter import Scrollbar, Label, Toplevel, ttk, messagebox
import csv
import os

class TasklistApp:
    def __init__(self):
        self.process_entry = None

        self.window = tk.Tk()
        self.window.title("輸入資訊")
        self.window.geometry("1000x600")

        # 將整體視窗分為上下兩個區域
        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(side=tk.TOP, pady=20)

        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # IP輸入
        ip_label = tk.Label(self.top_frame, text="IP:")
        ip_label.pack(side=tk.LEFT, padx=10)
        self.ip_entry = tk.Entry(self.top_frame)
        self.ip_entry.pack(side=tk.LEFT)
        self.ip_entry.focus()  # 將焦點設定在IP輸入框上

        # 使用者名稱輸入
        user_label = tk.Label(self.top_frame, text="User:")
        user_label.pack(side=tk.LEFT, padx=10)
        self.user_entry = tk.Entry(self.top_frame)
        self.user_entry.pack(side=tk.LEFT)

        # 密碼輸入
        password_label = tk.Label(self.top_frame, text="Password:")
        password_label.pack(side=tk.LEFT, padx=10)
        self.password_entry = tk.Entry(self.top_frame, show="*")
        self.password_entry.pack(side=tk.LEFT)

        self.submit_button = tk.Button(self.top_frame, text="Submit", command=self.show_tasklist)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.open_kill_button = tk.Button(self.top_frame, text="Kill Process", command=self.open_kill_window)
        self.open_kill_button.pack(side=tk.LEFT, padx=10)

        # 設定按下Enter鍵時觸發show_tasklist函式
        self.window.bind('<Return>', self.show_tasklist)

        # 表格部件
        self.tree_frame = tk.Frame(self.bottom_frame)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=20, expand=True)

        # 建立滚动条
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 連結滚动條與表格
        self.tree = ttk.Treeview(self.tree_frame, height=20, yscrollcommand=scrollbar.set)
        self.tree['show'] = 'headings'
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.configure(command=self.tree.yview)

        # 隱藏表格和滚动條
        self.tree_frame.pack_forget()

        # 添加表格单击事件
        self.tree.bind('<ButtonRelease-1>', self.handle_table_click)

    def show_tasklist(self, event=None):
        ip = self.ip_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        # 執行tasklist命令
        command = f"tasklist /S {ip} /U {user} /P {password}"
        result = os.popen(command).read()

        # csv
        command_csv = f"tasklist /s {ip} /u {user} /p {password} /fo csv > info/ram.txt"
        save_csv = os.system(command_csv)
        os.system('python csvprocess.py')

        # 讀取CSV檔案
        csv_path = "info/ram.csv"
        with open(csv_path, newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        # 清空表格
        self.tree.delete(*self.tree.get_children())

        # 設定表格列名
        columns = data[0]
        self.tree['columns'] = columns

        # 添加表格列名
        for col in columns:
            self.tree.heading(col, text=col)

        # 添加表格資料
        for row in data[1:]:
            self.tree.insert('', 'end', values=row)

        # 顯示表格和滚动條
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=20, expand=True)

        # draw
        os.system('python draw.py')

        # 建立第二個子視窗
        image_window = tk.Toplevel(self.window)
        image_window.title("RAM Usage: {}".format(ip))
        image_window.geometry("1100x450")

        # 建立圖片區域
        image_label = Label(image_window)
        image_label.pack()

        # 顯示圖片
        image_path = "info/ram.png"  # 將 "path_to_your_image.png" 替換為實際的圖片路徑
        image = tk.PhotoImage(file=image_path)
        image_label.configure(image=image)
        image_label.image = image  # 保持對圖片的引用，避免圖片被垃圾回收

    def handle_table_click(self, event):
        item = self.tree.focus()
        process_name = self.tree.item(item)["values"][0]
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to terminate the process '{process_name}'?")
        if confirmation:
            self.kill_process(process_name)

    def open_kill_window(self):
        ip = self.ip_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        # 建立子視窗
        kill_window = tk.Toplevel(self.window)
        kill_window.title("Kill Process: {}".format(ip))
        kill_window.geometry("300x200")

        # 輸入要終止的進程名稱
        process_label = tk.Label(kill_window, text="Process Name:")
        process_label.pack()
        self.process_entry = tk.Entry(kill_window)
        self.process_entry.pack()
        self.process_entry.focus()

        # 執行終止進程的按鈕
        kill_button = tk.Button(kill_window, text="Kill Process", command=self.kill_process_entry)
        kill_button.pack(pady=10)

        # 顯示結果的標籤
        self.result_label = tk.Label(kill_window, text="")
        self.result_label.pack()

    def kill_process_entry(self):
        process_name = self.process_entry.get()
        self.kill_process(process_name)

    def kill_process(self, process_name):
        ip = self.ip_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        # 執行taskkill命令
        command = f"taskkill /s {ip} /u {user} /p {password} /f /im {process_name}"
        result = os.popen(command).read()

        # 顯示結果
        self.result_label.config(text=result)

app = TasklistApp()
app.window.mainloop()

import tkinter as tk
import wmi
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import time
import os
import subprocess


class TasklistApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("遠端資源使用率")
        self.window.geometry("800x600")

        # IP輸入
        ip_label = tk.Label(self.window, text="IP:")
        ip_label.pack()
        self.ip_entry = tk.Entry(self.window)
        self.ip_entry.pack()
        self.ip_entry.focus()

        # 使用者名稱輸入
        user_label = tk.Label(self.window, text="User:")
        user_label.pack()
        self.user_entry = tk.Entry(self.window)
        self.user_entry.pack()

        # 密碼輸入
        password_label = tk.Label(self.window, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        # 開始監控按鈕
        start_button = tk.Button(self.window, text="Start Monitoring", command=self.start_monitoring)
        start_button.pack(pady=10)
        self.window.bind('<Return>', self.start_monitoring)

        # 建立滾動條
        scrollbar = ttk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 建立表格
        self.tree = ttk.Treeview(self.window, yscrollcommand=scrollbar.set)
        self.tree.pack(expand=True, fill=tk.BOTH)

        # 設定滾動條與表格的連動
        scrollbar.config(command=self.tree.yview)

        # 設定表格列名
        self.tree['show'] = 'headings'
        self.tree['columns'] = ('Name', 'MemoryUsage', 'CPUUsage')
        self.tree.heading('Name', text='Process Name')
        self.tree.heading('MemoryUsage', text='Memory Usage (MB)')
        self.tree.heading('CPUUsage', text='CPU Usage (%)')

        # 綁定表格點選事件
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)


    def start_monitoring(self, event=None):
        ip = self.ip_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        # 建立 WMI 連線
        connection = wmi.WMI(computer=ip, user=user, password=password)        

        # 調整視窗尺寸以確保能夠顯示所有的進程
        self.window.geometry("800x600")

        # 創建子窗口
        graph_window = tk.Toplevel(self.window)
        graph_window.title("Resource Usage Graph")
        graph_window.geometry("1200x600")
        
        # 創建日期資料夾
        info_folder = "info"
        date = time.strftime("%Y-%m-%d")
        date_folder = os.path.join(info_folder, date)
        if not os.path.exists(date_folder):
            os.mkdir(date_folder)

        # 創建遠端電腦IP名稱的資料夾
        ip_folder = os.path.join(date_folder, ip)
        if not os.path.exists(ip_folder):
            os.mkdir(ip_folder)

        # 創建圖表資料夾
        draw_folder = os.path.join(ip_folder, "chart")
        if not os.path.exists(draw_folder):
            os.mkdir(draw_folder)

        # 創建表格資料夾
        table_folder = os.path.join(ip_folder, "table")
        if not os.path.exists(table_folder):
            os.mkdir(table_folder)

        # 創建csv資料夾
        csv_folder = os.path.join(ip_folder, "csv")
        if not os.path.exists(csv_folder):
            os.mkdir(csv_folder)

        # 創建圖表
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 監控進程記憶體使用量和CPU使用率
        count = 0
        while True:
            processes = list(connection.Win32_PerfFormattedData_PerfProc_Process())
            processes.sort(key=lambda x: int(x.WorkingSetPrivate), reverse=True)

            # 清除表格內容
            if self.tree:
                self.tree.delete(*self.tree.get_children())

            process_data = defaultdict(lambda: [0, 0])  # 使用defaultdict建立字典，初始值為[0, 0]

            for process in processes:
                process_name = process.Name.split('#')[0]  # 取得程式名稱（排除 # 字號之後的部分）
                memory_usage = int(process.WorkingSetPrivate) // 1024 // 1024 # 轉換為MB
                cpu_usage = float(process.PercentProcessorTime)

                # 將記憶體使用量和CPU使用率加總
                process_data[process_name][0] += memory_usage
                process_data[process_name][1] += cpu_usage

            for process_name, (memory_usage, cpu_usage) in process_data.items():
                # 插入表格資料，只顯示加總後的結果
                self.tree.insert('', 'end', values=(process_name, memory_usage, cpu_usage))
            
            processes.clear()
            
            # 清除原有圖表内容
            for axis in ax:
                axis.clear()

            # 取得記憶體與CPU使用量前十名的程式資料
            top_memory = sorted(process_data.items(), key=lambda x: x[1][0], reverse=True)[:10]
            top_cpu = sorted(process_data.items(), key=lambda x: x[1][1], reverse=True)[:10]

            # 取得記憶體與CPU使用量前十名的程式名稱和資料
            top_process_names_memory = [process[0] for process in top_memory]
            top_memory_usages = [process[1][0] for process in top_memory]
            top_process_names_cpu = [process[0] for process in top_cpu]
            top_cpu_usages = [process[1][1] for process in top_cpu]

            # 繪製記憶體使用率柱狀圖
            ax[0].bar(top_process_names_memory, top_memory_usages)
            ax[0].set_xlabel('Process Name')
            ax[0].set_ylabel('Memory Usage (MB)')
            ax[0].set_title('Memory Usage')

            # 繪製CPU使用率柱狀圖
            ax[1].bar(top_process_names_cpu, top_cpu_usages)
            ax[1].set_xlabel('Process Name')
            ax[1].set_ylabel('CPU Usage (%)')
            ax[1].set_title('CPU Usage')

            # 在柱狀圖上顯示數值
            for i, v in enumerate(top_memory_usages):
                ax[0].text(i, v, str(v), ha='center', va='bottom')
            for i, v in enumerate(top_cpu_usages):
                ax[1].text(i, v, str(v), ha='center', va='bottom')

            # 調整子圖間距
            plt.subplots_adjust(hspace=0.5)

            # 更新圖表
            canvas.draw()

            # save draw
            current_time = time.strftime("%H-%M-%S")
            file_name = os.path.join(draw_folder, f"{current_time}.png")
            fig.savefig(file_name)

            # save table
            current_time = time.strftime("%H-%M-%S")
            file_name = os.path.join(table_folder, f"{current_time}.txt")
            with open(file_name, 'w') as f:
                for item in self.tree.get_children():
                    process_name = self.tree.item(item)['values'][0]
                    memory_usage = self.tree.item(item)['values'][1]
                    cpu_usage = self.tree.item(item)['values'][2]
                    f.write(f"Process Name:\t{process_name}\nMemory Usage:\t{memory_usage} MB\nCPU Usage:\t{cpu_usage} %\n\n")
            
            # save table
            current_time = time.strftime("%H-%M-%S")
            file_name = os.path.join(csv_folder, f"{current_time}.csv")
            with open(file_name, 'w') as f:
                f.write(f"Process Name,Memory Usage(MB),CPU Usage(%)\n")
                for item in self.tree.get_children():
                    process_name = self.tree.item(item)['values'][0]
                    memory_usage = self.tree.item(item)['values'][1]
                    cpu_usage = self.tree.item(item)['values'][2]
                    f.write(f"{process_name},{memory_usage},{cpu_usage}\n")

            '''
            # 約5分鐘儲存一次 (資料約每10秒更新一次)
            if count % 30 == 0:
                # save draw
                current_time = time.strftime("%H-%M-%S")
                file_name = os.path.join(draw_folder, f"{current_time}.png")
                fig.savefig(file_name)

                # save table
                current_time = time.strftime("%H-%M-%S")
                file_name = os.path.join(table_folder, f"{current_time}.txt")
                with open(file_name, 'w') as f:
                    for item in self.tree.get_children():
                        process_name = self.tree.item(item)['values'][0]
                        memory_usage = self.tree.item(item)['values'][1]
                        cpu_usage = self.tree.item(item)['values'][2]
                        f.write(f"Process Name:\t{process_name}\nMemory Usage:\t{memory_usage} MB\nCPU Usage:\t{cpu_usage} %\n\n")
            '''

            #print(count, time.strftime("%H-%M-%S"))
            for item in self.tree.get_children():
                    process_name = self.tree.item(item)['values'][0]
                    memory_usage = self.tree.item(item)['values'][1]
                    cpu_usage = self.tree.item(item)['values'][2]
                    print("Process Name:\t{}\nMemory Usage:\t{} MB\nCPU Usage:\t{} %\n\n".format(process_name, memory_usage, cpu_usage))
            count += 1
            

            self.window.update()
            #time.sleep(2)
            #self.window.after(300, self.start_monitoring)
            

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            process_name = self.tree.item(selected_item)['values'][0]
            confirmation = tk.messagebox.askyesno("Confirmation", f"Are you sure you want to close the process '{process_name}'?")
            if confirmation:
                ip = self.ip_entry.get()
                user = self.user_entry.get()
                password = self.password_entry.get()
                subprocess.run(["taskkill", "/s", ip, "/u", user, "/p", password, "/f", "/im", process_name + '.exe'])



app = TasklistApp()
app.window.mainloop()

# -*- coding: utf-8 -*-
import psutil

print('cpu count: ', psutil.cpu_count(logical=False),  # 實際物理 CPU 數量
    '<br>logical: ', psutil.cpu_count(),               # CPU 邏輯數量
    '<br>cpu percent: ', psutil.cpu_percent(interval=0.5, percpu=True), # CPU   使用率
                                                     # interval:每隔多少秒更新一次
                                                     # percpu:查看所有 CPU 使用率
    '<br>cpu freq: ', psutil.cpu_freq())                # CPU 使用頻率
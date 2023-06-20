import psutil
from pprint import pprint
from itertools import zip_longest
''' 
# CPU info
print(psutil.cpu_count())               # CPU 邏輯數量
print(psutil.cpu_count(logical=False))  # 實際物理 CPU 數量
print(psutil.cpu_percent(interval=0.5, percpu=True)) # CPU   使用率
                                                     # interval:每隔多少秒更新一次
                                                     # percpu:查看所有 CPU 使用率
print(psutil.cpu_freq())                # CPU 使用頻率
'''

#print(psutil.virtual_memory())  # 記憶體資訊
#print(psutil.virtual_memory().percent) # 記憶體使用量
#print(psutil.virtual_memory().available) # 所有記憶體大小



# 查看所有程式的 RAM 使用資訊
'''
prcs_id = []
for prcs in psutil.process_iter():
    #print(prcs)           # 印出所有正在執行的應用程式 ( 從中觀察 pid )
    prcs_id.append(prcs._pid)
for id in prcs_id:
    p = psutil.Process(pid=id)
    print(id , ':\n', p.memory_info())
'''

procs = [(proc.info['name'], proc.info['memory_info']) for proc in psutil.process_iter(attrs=['name', 'memory_info'])]

'''
def split_list(l, n):
  # 將list分割 (l:list, n:每個matrix裡面有n個元素)
  for idx in range(0, len(l), n):
    yield l[idx:idx+n]
result = list(split_list(procs, 1,))
'''
raminfo = []
line = str('<br><br>')

def group_elements(n, iterable, padvalue='x'):
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

for output in group_elements(1,procs):
    #print(output)
    raminfo.append(output)
    raminfo.append(line)
print(raminfo)

#print(procs)
    # rss: 實際記憶體使用量
    # vms: 虛擬記憶體使用量



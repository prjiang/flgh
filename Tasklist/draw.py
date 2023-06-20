import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('info/ram.csv', encoding='big5')

df = df.drop(columns=['PID'])

dataset = df.loc[:].head(10) # .loc[:] -> avoid getting the SettingWithCopyWarning
dataset.sort_values(by=['RAM'], ascending=True, inplace=True)
dataset.set_index('Task', inplace=True)

chart = dataset.plot(kind='barh',
                    title='',
                    xlabel='RAM (K)',
                    ylabel='Task\n',
                    legend=True,
                    figsize=(10,5),
                    )

#plt.show()
plt.savefig('info/ram.png', bbox_inches='tight')

'''
# 取得 CPU 欄位中數字最大的前 10 筆資料
cpu_dataset = df.nlargest(10, 'CPU')

# 將取得的資料進行排序，以符合圖形需求
cpu_dataset.sort_values(by=['CPU'], ascending=True, inplace=True)
cpu_dataset.set_index('Task', inplace=True)



# 保存圖形
plt.savefig('info/ram_cpu.png', bbox_inches='tight')
'''
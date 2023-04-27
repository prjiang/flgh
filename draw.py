import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('info/test.csv', encoding='big5')

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
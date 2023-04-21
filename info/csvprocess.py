import pandas as pd

df = pd.read_csv('test.txt', encoding = 'big5')

ram = df[df.columns[-1]].str.strip('K')

'''
test = filter(str.isdigit,a)
int("".join(list(test)))
'''

df.insert(2,'RAM',ram)
df.sort_values(by=['RAM','PID'], ascending=True)

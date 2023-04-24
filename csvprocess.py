import pandas as pd

df = pd.read_csv('info\\test.txt', encoding = 'big5')

ram_str = df[df.columns[-1]].str.strip('K')
ram_str = ram_str.str.replace(',','',1)
ram = ram_str.astype('int')

'''
test = filter(str.isdigit,a)
int("".join(list(test)))
'''

df.insert(2,'RAM',ram)
df.sort_values(by=['RAM'], ascending=True, inplace=True)
df.to_csv('info\\test.csv', index=False, encoding='big5')
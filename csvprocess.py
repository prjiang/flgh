import pandas as pd

''' txt to csv
import csv

csvfile = open("info/ram.csv","w",newline="")
writer = csv.writer(csvfile)
csvrow = []

f = open("info/ram.txt","r")
for line in f:
    csvrow = line.split()
    writer.writerow(csvrow)

f.close()
csvfile.close()
'''

df = pd.read_csv('info\\ram.txt', encoding = 'big5')

ram_str = df[df.columns[-1]].str.strip('K')
ram_str = ram_str.str.replace(',','',1)
ram = ram_str.astype('int')

df.insert(2,'RAM',ram)
df.sort_values(by=['RAM'], ascending=False, inplace=True)
df = df.drop(columns=['工作階段名稱','工作階段 #','RAM使用量'])

columns = ['映像名稱']
df = df.drop_duplicates(subset=columns, keep='first')

df.to_csv('info\\ram.csv', index=False, encoding='big5')

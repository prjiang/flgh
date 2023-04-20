import csv
csvfile = open("info/test.csv","w",newline="")
writer = csv.writer(csvfile)
csvrow = []

f = open("info/test.txt","r")
for line in f:
    csvrow = line.split()
    writer.writerow(csvrow)

f.close()
csvfile.close()
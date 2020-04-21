s1 = "https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/501436763/"

fin = open('links_jan_11-31.txt','r')
fout = open('links_jan_11-31_for_dl.csv','w')

for line in fin:
    ls = line.split(',')
    fout.write(s1+ls[0]+'\n')
    
fin.close()
fout.close()
s1 = "https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/501436358/"

fin = open('south_america_2w_v3_links.txt','r')
fout = open('south_america_2w_v3_dl_links.csv','w')

for line in fin:
    ls = line.split(',')
    fout.write(s1+ls[0]+'\n')
    
fin.close()
fout.close()
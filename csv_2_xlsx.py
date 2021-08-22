import pandas as pd
import os
import glob


dir_l = input("Location : ")

os.chdir(dir_l)

pattern ='*.csv'
xllis=glob.glob(pattern)
# xllis = os.listdir(pp)
# xllis.sort()
print(xllis)



# data = pd.read_csv("k.csv")

# data.to_excel("new_file.xlsx", index=None, header=True)
import os

""" 
Renames the filenames within the same directory to "mountain_lion_num.jpg"
"""

file = open('trainval.txt','w')

path =  os.getcwd()
print(path)
path = path + "/images"
files = os.listdir(path)

for f in files:
    file.write(f + " 1 1 1\n") 
    
file.close()
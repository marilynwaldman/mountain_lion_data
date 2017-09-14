import os

""" 
Renames the filenames within the same directory to "mountain_lion_num.jpg"
"""

file = open('annotations/trainval.txt','w')

path =  os.getcwd()
print(path)
path = path + "/images"
files = os.listdir(path)

for f in files:
    filename, file_extension = os.path.splitext(f)	    
    file.write(filename + " 1 1 1\n") 
    
file.close()
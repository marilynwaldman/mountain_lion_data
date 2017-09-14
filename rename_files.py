import os

""" 
Renames the filenames within the same directory to "mountain_lion_num.jpg"
"""

path =  os.getcwd()
print(path)
path = path + "/images"
files = os.listdir(path)
i = 1

for file in files:
    filename, file_extension = os.path.splitext(file)
    os.rename(os.path.join(path, file), os.path.join(path, "mountain_lion_" + str(i) + file_extension))
    i = i+1
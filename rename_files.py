import os
import sys, getopt

""" 
Renames the filenames within the same directory to "mountain_lion_num.jpg"
"""

def main(argv):
   inputdir = ''
   member = ''
   try:
      opts, args = getopt.getopt(argv,"hi:m:",["idir=","imem="])
   except getopt.GetoptError:
      print 'test.py -i <inputdir>  -m <member>'
      sys.exit(2)
   print(len(opts))
   if len(opts) != 2:
        print 'USAGE:  rename_files.py -i <inputdir>  -m <member>'
        sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputdir>  -m <member>'
         sys.exit()
      elif opt in ("-i", "--idir"):
         inputdir = arg
      elif opt in ("-m", "--imem"):
          member = arg
     
   print 'Input file is "', inputdir
   print 'Member is "', member
     
   path =  os.getcwd() + '/' + inputdir
     
   files = os.listdir(path)
   i = 1
   for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg' :
            os.rename(os.path.join(path, file), os.path.join(path, member + '_' + str(i) + file_extension))
        i = i+1

if __name__ == "__main__":
   main(sys.argv[1:])

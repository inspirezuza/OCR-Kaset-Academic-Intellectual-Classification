from os.path import isdir

#folder_path
folder_path = open('setup.txt').readline()
if not isdir(folder_path):
  print("หาตำแหน่งไฟล์ไม่เจอ ลองแก้ใน setup.txt")
  import sys
  sys.exit()

#stop
file_amount = -1
debug = False

#start
import time
print('program start in 3 seconds')
time.sleep(3)
from module import *
start(folder_path,stop=file_amount,DEBUG=debug)
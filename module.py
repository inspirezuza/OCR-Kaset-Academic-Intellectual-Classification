import os
import pytesseract

from pdf2image import convert_from_path, convert_from_bytes
from IPython.display import display, Image

#folder_path
folder_path = open('setup.txt').readline()
if not os.path.isdir(folder_path):
  print("หาตำแหน่งไฟล์ไม่เจอ ลองแก้ใน setup.txt")
  import sys
  sys.exit()

#filename_to_img
size_img = 1200
ppath_from_install = os.getcwd() + r'\installation\poppler-22.04.0\Library\bin'

#tesseract
pytesseract.pytesseract.tesseract_cmd = os.getcwd() + r'\installation\tesseract\tesseract.exe'

#crop img
header_offset = 0
footer_offset = 600 

#nametype
zero_one = ['เนินโ']
zero_two = ['เปลี่ยนแปลง'] 
zero_three = ['ปิด', 'มก.พว.03'] 
zero_four = ['ขยาย'] 

#renamefile
acc = False

def folder_path_to_files(folder_path):
  files = []
  for file in os.listdir(folder_path):
    files.append(file)
  return files

def filename_to_img(folder_path, file_name):
  path = folder_path + '/' + file_name
  images = convert_from_path(path, size=size_img, single_file=True, grayscale=True, fmt="jpg",
                            poppler_path = ppath_from_install)
  return images[0]

def crop_img(img):
  return img.crop((0, header_offset, img.width, footer_offset))

def thai_to_arabic(s): 
    
  thai = ['๐','๑','๒','๓','๔','๕','๖','๗','๘','๙']
  ns = ''
  for c in s:
    checkthai = False

    for i in range(10):

      if thai[i] == c:
        checkthai = True
        ns += str(i)
        break

    if not checkthai:
      ns += c

  return ns

def polish_string_data(raw_string_data):
  return raw_string_data.replace('\n', '')

def for_i_in_s(l,s):
  for i in l:
    if i in s:
      return True
  return False

def name_type(string_data):
  file_name = ''

  #โอนงวด
  if 'โอน' in string_data or 'ดสรร' in string_data:
    file_name += 'โอนงวด'
    if 'งวดที่' in string_data:
      result = ' '
      tpos = string_data.find('งวดที่')
      if string_data[tpos+7].isnumeric():
        result += string_data[tpos+7]
      if string_data[tpos+8].isnumeric():
        result += string_data[tpos+8]
      if string_data[tpos+9].isnumeric():
        result += string_data[tpos+9]
      if len(result) != 1:
        file_name += result

      file_name = thai_to_arabic(file_name)

  #04
  elif for_i_in_s(zero_four,string_data):
    file_name += '04'
    if 'ครั้งที' in string_data:
      sf = string_data.find('ครั้งที')
      result = '('
      if string_data[sf+8].isnumeric():
        result += string_data[sf+8]
      if string_data[sf+9].isnumeric():
        result += string_data[sf+9]
      if string_data[sf+10].isnumeric():
        result += string_data[sf+10]
      if string_data[sf+11].isnumeric():
        result += string_data[sf+11]
      
      if len(result) != 1:
        file_name += result + ')'    
        file_name = thai_to_arabic(file_name)

  #01
  elif for_i_in_s(zero_one,string_data):
    file_name += '01'

  #02
  elif for_i_in_s(zero_two,string_data):
    file_name += '02'

  #03
  elif for_i_in_s(zero_three,string_data):
    file_name += '03'

  return file_name

def name_regis_number(string_data):
  file_name = ''
  for idx,i in enumerate(string_data):
    if i == '/' and string_data[idx-3:idx].isnumeric() and string_data[idx+1:idx+3].isnumeric():
      if string_data[idx+1] in ['5','6']:
        file_name += '00' + string_data[idx-3:idx] + '-' + string_data[idx+1:idx+3]
        break
  if file_name == '': return file_name  
  file_name = thai_to_arabic(file_name)
  return ' ' + file_name

def sinl(s,l):
  for i in l[1:]:
    if i in s:
      return True
  return False

agency_list = [s.split(", ") for s in [i.replace('\n','') for i in open('agency.txt', encoding="utf8").readlines()]]
def name_agency(string_data):
  for l in agency_list:
    if sinl(string_data,l):
      return ' ' + l[0]
  return ''

def name_location(string_data):
  if 'แพงแสน' in string_data:
    return ' กพส.'
  elif 'ศรีราชา' in string_data:
    return ' ศรีราชา'
  else: #บางเขน
    return ''

# acc = False
def rename_file(string_data,DEBUG = False):
    acc = False
    if DEBUG == False:
        nregis_number = name_regis_number(string_data)
        if nregis_number == '': return ('',False)

        ntype = name_type(string_data)
        if ntype == '': return ('',False)

        nagency = name_agency(string_data)
        if nagency == '': return ('',False)

        nlocation =  name_location(string_data)
        acc = True
    elif DEBUG == True:
        ntype = name_type(string_data)
        nregis_number = name_regis_number(string_data)
        nagency = name_agency(string_data)
        nlocation =  name_location(string_data)
        if ntype != '' and nregis_number != '' and nagency != '':
            acc = True

    file_name = ''.join([ntype, nregis_number, nagency, nlocation])
    return (file_name,acc)

def is_filename_new(filename, DEBUG):
    if DEBUG: return True
    if filename[:-9].isnumeric():
        return True
    return False

def start(folder_path, stop=-1, DEBUG=False):
  count = 0
  #start
  files = folder_path_to_files(folder_path)
  i = 1
  for filename in files:
    print(str(i) + ' ' + filename,end = "")
    if not is_filename_new(filename, DEBUG):
        print(' already rename')
        i += 1
        continue
    #1
    images = []
    img = filename_to_img(folder_path, filename)
    cimg = crop_img(img)

    #2
    raw_string_data = pytesseract.image_to_string(cimg, 'tha')

    #3
    string_data = polish_string_data(raw_string_data)
    newname = rename_file(string_data,False)[0]
    print(rename_file(string_data))

    print(" | " + newname)

    #4
    if rename_file(string_data,False)[1]:
        count+=1
        old_name = folder_path + r"\\" + filename
        new_name = folder_path + r"\\" + newname + '.pdf'

        if os.path.isfile(new_name):
            print("The file already exists")
        else:
            # Rename the file
            os.rename(old_name, new_name)

    if i==stop:
      break
    i += 1

  print(f'finish rename > {count}')
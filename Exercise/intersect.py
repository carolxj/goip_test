import sys,os
import xlrd
# import pandas as pd
# import numpy as np


if len(sys.argv) < 4:
  print("usage: intersect.py in_file1[[,sheet_index],column_index] in_file2[[,sheet_index],column_index] out_file")
  os.system("pause")
  sys.exit()

class ExcelCol:
  def __init__(self, filename):
    fpars = filename.split(',')
    
    self.file = fpars[0]
    self.sheet = 0
    self.index = 0
    
    if len(fpars) >= 3:
      self.sheet = int(fpars[1]) - 1
      self.index = int(fpars[2]) - 1
    elif len(fpars) >= 2:
      self.index = int(fpars[1]) - 1
      
    df = pd.read_excel(self.file, sheet_name=self.sheet, header=None, usecols=[self.index], names=['order'], engine='openpyxl')

col1 = ExcelCol(sys.argv[1])
col2 = ExcelCol(sys.argv[2])

df3 = pd.concat([col1.df, col2.df, col2.df]).drop_duplicates(keep=False)
writer = pd.ExcelWriter(os.path.dirname(col1.file) + '\\' + sys.argv[3] + '.xlsx')

df3.to_excel(writer, index=None)
writer.save()
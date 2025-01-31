import tkinter
from tkinter import filedialog
import os
import pandas as pd

from verify_key_errors import main

tables = 'lu'.split('; ') #files that need correction

keys_delete = 'teste'.split('; ') #lines with this key will be deleted

#insert manually all the references that need to be fixed
# {wrong_name : new_name}
keys_rename = {' Promissao_08_2022_Ponto_22' : 'Promissao_08_2022_Ponto_22',
               ' Promissao_08_2022_Ponto_18' : 'Promissao_08_2022_Ponto_18',
               ' Promissao_08_2022_Ponto_03' : 'Promissao_08_2022_Ponto_03',
               ' Promissao_08_2022_Ponto_01' : 'Promissao_08_2022_Ponto_01',
               ' Promissao_08_2022_Ponto_08' : 'Promissao_08_2022_Ponto_08',
               ' Promissao_08_2022_Ponto_19' : 'Promissao_08_2022_Ponto_19'}

root = tkinter.Tk()
root.withdraw()

sheet_dir = filedialog.askdirectory()
if not sheet_dir:
    exit()

for folder in os.listdir(sheet_dir):
    name = folder[:-4]
    if name in 'estacoes campanhas'.split(): #
        continue
    path = os.path.join(sheet_dir, folder)

    data_frame = None
    delims = ', ;'.split()
    for delim in delims:
        try:
            data_frame = pd.read_csv(path, delimiter=delim, decimal= '.', encoding='ISO-8859-1', index_col = 0)
            if data_frame.shape[1] <= 1:
                data_frame = None
            else: break
        except: continue

    try:
        data_frame = data_frame.dropna(subset=['estacoes_id'])
    except:
        print(f'dataframe {name} vazio')
            
    if name in tables:
        data_frame = data_frame[~data_frame['estacoes_id'].isin(keys_delete)]
      
        for key in keys_rename:
            value = keys_rename[key]
            data_frame.loc[data_frame['estacoes_id'] == key, 'estacoes_id'] = value
    
        with open(path, 'w') as file:
            print(f'escrevendo {name}')
            file.write(data_frame.to_csv())


#MAIN APPLICATION
main(sheet_dir)
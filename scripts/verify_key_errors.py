import tkinter
from tkinter import messagebox, filedialog
import os
import pandas as pd
import re

def build_dataframe(file_path):
    data_frame = None
    name = None
    try:
        for delim in [',', ';']:
            try:
                data_frame = pd.read_csv(file_path, delimiter=delim, decimal='.', encoding='ISO-8859-1', index_col=0)
                if data_frame.shape[1] <= 1:
                    data_frame = None
                else:
                    break
            except:
                continue
    except:
        messagebox.showerror('Erro', f'Arquivo {file_path} nao foi lido corretamente')

    #extracting filename
    pattern = r'.*\\(.*)\..*$'
    match = re.search(pattern, file_path)
    name = match.group(1)
    if data_frame.iloc[:,0].name not in ['estacoes_id', 'campanha_id']:
        data_frame = pd.read_csv(file_path, delimiter=delim, decimal='.', encoding='ISO-8859-1')
    return data_frame, name

def main(path):
    paths = []
    campanhas_frame = None
    estacoes_frame = None

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if '.csv' not in file:
            messagebox.showerror('Erro', f'Arquivo {file} nao e um ".csv"')
            exit()
        if 'campanhas' in file:
            campanhas_frame, name = build_dataframe(file_path)
        elif 'estacoes' in file:
            estacoes_frame, name = build_dataframe(file_path)
            estacoes_frame = estacoes_frame.rename(columns={'estacoes_id':'estacao_nome'})
        else:
            paths.append(file_path)

    campanhas_keys = sorted(set(campanhas_frame['campanha_nome'].values)) # 'campanhas.csv' keys
    estacoes_keys = sorted(set(estacoes_frame['estacao_nome'].values)) # 'estacoes.csv' keys
    estacoes_references = sorted(set(estacoes_frame['campanha_id'].values)) # 'campanhas.csv' references

    working_dir = os.getcwd()

    #extracting folder name
    pattern = r'.*\/(.*)$'
    if batch:
        pattern = r'.*[\\/](.*)$'
    match = re.search(pattern, path)
    folder_name = match.group(1)

    #txt to register all the errors
    log_path = os.path.join(working_dir, f'error_logs/{folder_name}_error_log.txt')

    with open (log_path, 'w') as arquivo:
        #check all references in 'estacoes.csv' that do not match 'campanhas.csv' keys
        estacoes_errors = []
        for key in estacoes_references:
            if key not in campanhas_keys:
                estacoes_errors.append(f'Chave {key} nao encontrada na tabela campanhas\n')
        
        if len(estacoes_errors) == 0:
            arquivo.write('Nenhum erro na tabela estacoes foi detectado\n---------\n')
        else:
            for error in estacoes_errors:
                arquivo.write(error)
            arquivo.write(f'\nFim da tabela estacoes\n---------\n')

        #check all other tables references that do not match 'estacoes.csv' keys
        for file in paths:
            measure_errors = []
            measure_frame, measure_name = build_dataframe(file)
            print(measure_name)
            if 'id' in measure_frame.columns:
                measure_frame = measure_frame.drop(columns=['id'])

            arquivo.write(f'Erros da tabela {measure_name}\n---------\n')

            references = None
            
            measure_frame.columns = measure_frame.columns.astype(str)
            references = set(measure_frame['estacoes_id'].values)
            

            for reference in references:
                if reference not in estacoes_keys:
                    measure_errors.append(f'Chave {reference} nao esta na tabela estacoes\n')


            if len(measure_errors) == 0:
                arquivo.write(f'Nenhum erro na tabela {measure_name} foi detectado\n---------\n')
            else:
                for error in measure_errors:
                    arquivo.write(error)
                arquivo.write(f'\nFim da tabela {measure_name}\n---------\n')


#MAIN APPLICATION
#some table had wrong written references, therefore the need to fix
batch = False

if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()
    sheet_dir = filedialog.askdirectory(initialdir=r'C:\Users\Usuario\Downloads\dados_banco')

    if not sheet_dir:
        exit()

    batch = messagebox.askyesno('Opção', 'Deseja processar os arquivos em lote ?')

    if batch:
        for folder in os.listdir(sheet_dir):
            newPath = os.path.join(sheet_dir, folder)
            main(newPath)
    else:
        main(sheet_dir)

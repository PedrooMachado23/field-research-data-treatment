from sqlalchemy import create_engine, inspect
import pandas as pd
import tkinter
from tkinter import messagebox, filedialog
import os
import numpy as np
from dotenv import load_dotenv

#padronizing error message
def error_message(message):
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showerror('Erro', message)

#connecting to db
def get_engine_conn():

    #loading vars
    load_dotenv()
    database = os.getenv('DATABASE')
    user = os.getenv('USER')
    passwd = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    
    try:
        conn_string = f'postgresql://{user}:{passwd}@{host}:{port}/{database}'
        engine = create_engine(conn_string)
        connection = engine.connect()
    except Exception as e:
        error_message('Não foi possível conectar na database')
        print(e)
        exit()
    return engine, connection

#build all file paths
def create_paths(folder_path):
    paths = []
    names = []

    for item in os.listdir(folder_path):
        if '.csv' not in item:
            error_message('Selecione apenas arquivos no formato csv')
            exit()

        name = item[:-4]
        item_path = os.path.join(folder_path, item)

        names.append(name)
        paths.append(item_path)
    
    def sort_rule(x):
        #those files have fkeys and need to be uploaded first
        return 0 if 'campanhas' in x else 1 if 'estacoes' in x else 2
    
    return sorted(paths, key=sort_rule), sorted(names, key=sort_rule)

#builds dataframes
def reading_data(path, name):
    data_frame = None
    delims = [',', ';'] #some files doesn't follow the delim ';' pattern
    for delim in delims:
            try:
                data_frame = pd.read_csv(path, delimiter=delim, decimal='.', encoding='ISO-8859-1', index_col=0)
                if data_frame.shape[1] <= 1:
                    if delim == ';':
                        error_message(f'Erro: Arquivo {name} não foi lido corretamente')
                        exit() 
                    data_frame = None
                else:
                    break
            except:
                continue
    if data_frame.iloc[:,0].name not in ['estacoes_id', 'campanha_id']:
        data_frame = pd.read_csv(path, delimiter=delim, decimal='.', encoding='ISO-8859-1')
    try:
        #some datetimes appears in the wrong format
        if data_frame['DateTime'].str.endswith('Z').any():
            data_frame['DateTime'] = pd.to_datetime(data_frame['DateTime']).dt.strftime('%Y-%m-%d %H:%M:%S')
    except: pass

    data_frame.columns = data_frame.columns.str.lower()
    df_columns = data_frame.columns.tolist()

    #default padronization for tables that have wrong column names
    columns_to_rename = {'pressure' : 'profundidade',
                         'estacoes_id' : 'estacao_nome',
                         'tempo' : 'datetime',
                         'acdom' : 'acdom440'}

    for col_name in columns_to_rename:
        if col_name in df_columns:
            if col_name == 'pressure':
                #some tables would have text instead of NaN or a number
                data_frame['pressure'] = data_frame['pressure'].apply(lambda x: np.nan if isinstance(x, str) else x)
                #this specific filename is correctly named
            if col_name == 'estacoes_id' and name != 'estacoes':
                continue
            data_frame = data_frame.rename(columns={col_name : columns_to_rename[col_name]})

    return data_frame

#get all column names from the table schema
def get_schema(table, engine):
    inspector = inspect(engine)
    columns = inspector.get_columns(table)
    column_names = [col['name'] for col in columns if col['name'] not in ['id', 'geom']]  # Exclude 'id, geom' column
    return column_names

def main(archive_dir):
    engine, connection = get_engine_conn()
    paths, names = create_paths(archive_dir)

    for index in range(len(paths)):
        path = paths[index]
        name = names[index]

        data_frame = reading_data(path, name)

        table_columns = get_schema(name, engine)
        #match the columns to maintain the correct order and to delete uneccessary old columns
        table_columns_match = [x for x in table_columns if x in data_frame.columns] #tables that are both in dataframe and table
        data_frame = data_frame[table_columns_match]

        data_frame.to_sql(name=name, con=engine, if_exists='append', index=False)
        if (batch):
            print(f'Pasta: {folder} tabela {name} atualizada')
        else:
            print(f'Tabela {name} atualizada!')

#MAIN APPLICATION
if __name__ == '__main__':
    root = tkinter.Tk()
    root.withdraw()

    sheet_dir = filedialog.askdirectory()

    if not sheet_dir:
        exit()

    #asking if multiple dirs will be processed
    batch = messagebox.askyesno('Opção', 'Deseja processar os arquivos em lote ?')

    if batch:
        for folder in os.listdir(sheet_dir):
            newPath = os.path.join(sheet_dir, folder)
            main(newPath)
    else:
        main(sheet_dir)
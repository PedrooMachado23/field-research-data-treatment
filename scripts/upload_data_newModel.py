import os
import tkinter
from tkinter import messagebox, filedialog
from sqlalchemy import inspect, select, column, text

from upload_data import create_paths, reading_data, get_engine_conn, get_schema

def get_keys(connection, table_name, table_column):
    #the change consist in transforming string pk into id, therefore the need to retrieve the name
    id_col = column('id')
    query = select(id_col, column(table_column)).select_from(text(table_name))

    query_result = connection.execute(query).fetchall()

    query_dict = {}
    for row in query_result:
        # {name : id}
        query_dict[row[1]] = row[0]
    

    return query_dict

def main(dir_path, folder_name):
    engine, connection = get_engine_conn()

    paths, names = create_paths(dir_path)

    camp_list = {}
    estac_list = None

    for index in range(len(paths)):
        path, name = paths[index], names[index]

        data_frame = reading_data(path, name)
        data_frame = data_frame.dropna(subset=[data_frame.columns[0]]) #drop some indexes with NaN value

        table_columns = get_schema(name, engine)
        table_columns_match = [x for x in table_columns if x in data_frame.columns and x != 'id']
        data_frame = data_frame[table_columns_match]

        #just to verify if the campaign is already inserted
        if name == 'campanhas':
            camp_list = get_keys(connection, table_name='campanhas', table_column='campanha_nome')
            if data_frame['campanha_nome'].isin(camp_list.keys()).any():
                break
        
        if name == 'estacoes':
            camp_list = get_keys(connection, table_name='campanhas', table_column='campanha_nome')
            #use the name to assign the id for the right fkey reference
            data_frame['campanha_id'] = data_frame['campanha_id'].apply(lambda value: camp_list[value] or 1)

        elif name != 'campanhas':
            if not estac_list:
                estac_list = get_keys(connection, table_name='estacoes', table_column='estacao_nome')
            data_frame['estacoes_id'] = data_frame['estacoes_id'].apply(lambda value: estac_list[value])
        
        data_frame.to_sql(name=name, con=engine, if_exists='append', index=False)
        print(f'Pasta {folder_name}, tabela {name} atualizada!')




#MAIN APPLICATION
#the database model has changed, so this file is to change the tables to the new format
#work similarly to 'upload_data.py'
root = tkinter.Tk()
root.withdraw()
target_dir = filedialog.askdirectory()

if not target_dir:
    exit()

for folder in os.listdir(target_dir):
    newPath = os.path.join(target_dir, folder)
    main(newPath, folder)
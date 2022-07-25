import os
import pandas as pd


def create_folder_if_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

def handle_level_file(level_file):
    try:
        sheets_dict = pd.read_excel(level_file, sheet_name=None)
        df=sheets_dict['CLIENTES']
        df_genero=sheets_dict['GENEROS']
        if df.columns.to_list()==['GRUPO','ALIAS','AINI','AFIN']and df_genero.columns.to_list()==['GENERO']:
            return df,df_genero['GENERO']
        else:
            print('Error with column names')
            return pd.DataFrame(),None
    except:
        return pd.DataFrame(),None

def scontab_tree(root, level_file):
    """
    This function creates a folder tree inside the specified root, according to the level excel file.
    """
    df,genders=handle_level_file(level_file)
    if df.empty:
        print('Error reading file')
        return
    path0=root
    lvl1=df['GRUPO'].unique()
    for l1 in lvl1:
        folders_l1=f'{l1}_CON'
        path1=path0+'/'+folders_l1
        create_folder_if_not_exist(path1)
        lvl2=df[df['GRUPO']==l1]['ALIAS']
        for l2 in lvl2:
            folders_l2=f'{l1}_[{l2}]_CON'
            path2=path1+'/'+folders_l2
            create_folder_if_not_exist(path2)
            iniyear=int(df[(df['GRUPO']==l1) & (df['ALIAS']==l2)]['AINI'].iloc[0])
            endyear=int(df[(df['GRUPO']==l1) & (df['ALIAS']==l2)]['AFIN'].iloc[0])
            for y in range(iniyear,endyear+1):
                l3=y-2000
                folders_l3=f'{l1}_[{l2}]_CON_{l3}'
                path3=path2+'/'+folders_l3
                create_folder_if_not_exist(path3)
                lvl4=genders
                for l4 in lvl4:
                    folders_l4=f'{l1}_[{l2}]_CON_{l4}_{l3}'
                    path4=path3+'/'+folders_l4
                    create_folder_if_not_exist(path4)
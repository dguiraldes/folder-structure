import os
import shutil
import pandas as pd

class folder_tree:

    def __init__(self,root,level_file,expected_columns,suffix):
        """
        root (str)              : Direction to main folder where tree is meant to be created
        level_file (str)        : direction to excel file containing tree structure
        expected_columns (dict) : dict with expected column by sheet. i.e. {'CLIENTES':{'GRUPO':'str','ALIAS':'str','AINI':'int','AFIN':'int'}}
        """
        self.root=root
        self.suffix=suffix
        self.expected_columns=expected_columns
        self.status='Inicializado'
        self.sheets_dict={}
        self.read_level_file(level_file)

    def read_level_file(self,level_file):
        try:
            for sheet in self.expected_columns.keys():
                sheet_df= pd.read_excel(level_file, sheet_name=sheet, converters=self.expected_columns[sheet])
                self.sheets_dict.update({sheet:sheet_df})
                self.status='OK'
        except Exception as e:
            self.status=f'Archivo invalido: Revisar nombre de arvhico, nombre de columnas o tipo de columnas\n Error: {e}'
    
    def check_df_headers(self):
        """
        Headers must be what is excpected
        """
        for sheet in self.expected_columns.keys():
            df_cols=self.sheets_dict[sheet]
            exp_cols=self.expected_columns[sheet].keys()
            if df_cols==exp_cols:
                self.status='OK'
            else:
                self.status=f'Error en nombre de columnas: Se esperaba {exp_cols},\n pero se ingresa {df_cols}'


    def create_folder_if_not_exist(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
            self.created_folders+=1

    @staticmethod
    def check_int_boundries(series,lower_bound,upper_bound):
        return (series>lower_bound).all() and (series<upper_bound).all()


class tree_type_1(folder_tree):

    def __init__(self,root,level_file,suffix,file_directory):
        """
        expected_columns (dict) : dict with expected column by sheet and its types
        """
        expected_columns={'CLIENTES':{'GRUPO':str,'ALIAS':str,'AINI':int,'AFIN':int},'NIVEL':{'CARPETA':str}}
        self.file_directory=file_directory
        super().__init__(root,level_file,expected_columns,suffix)
        if self.status!='OK': return
        self.check_year_boundries()
    
    def check_year_boundries(self):
        aini=self.sheets_dict['CLIENTES']['AINI']
        afin=self.sheets_dict['CLIENTES']['AFIN']
        checkaini=self.check_int_boundries(aini,2000,2100)
        checkafin=self.check_int_boundries(afin,2000,2100)
        checkboth=(afin>=aini).all()
        if checkaini and checkafin and checkboth:
            self.status='OK'
        elif not checkboth:
            self.status='AFIN siempre debe ser mayor que AINI'
        else:
            self.status='Revisar AINI o AFIN. Existen valores fuera del rango (2000, 2100)'

    def generate(self):
        """
        This function creates a folder tree inside the specified root, according to the level excel file.
        """
        ########################## Check if files are ok #################
        if self.status!='OK': return

        ########################## Initiate ########################## 
        path0=self.root
        self.created_folders=0
        df_clientes=self.sheets_dict['CLIENTES']
        df_generos=self.sheets_dict['NIVEL']

        ########################## Level 1 ###############################
        lvl1=df_clientes['GRUPO'].unique()
        for l1 in lvl1:
            folders_l1=f'{l1}_{self.suffix}'
            path1=path0+'/'+folders_l1
            self.create_folder_if_not_exist(path1)
        
        ########################## Level 2 ###############################
            lvl2=df_clientes[df_clientes['GRUPO']==l1]['ALIAS']
            for l2 in lvl2:
                folders_l2=f'{l1}_[{l2}]_{self.suffix}'
                path2=path1+'/'+folders_l2
                self.create_folder_if_not_exist(path2)
            
        ########################## Level 3 ###############################    
                iniyear=int(df_clientes[(df_clientes['GRUPO']==l1) & (df_clientes['ALIAS']==l2)]['AINI'].iloc[0])
                endyear=int(df_clientes[(df_clientes['GRUPO']==l1) & (df_clientes['ALIAS']==l2)]['AFIN'].iloc[0])
                for y in range(iniyear,endyear+1):
                    l3=y-2000
                    folders_l3=f'{l1}_[{l2}]_{self.suffix}_{l3}'
                    path3=path2+'/'+folders_l3
                    self.create_folder_if_not_exist(path3)
        
        ########################## Level 4 ###############################
                    lvl4=df_generos['CARPETA']
                    for l4 in lvl4:
                        folders_l4=f'{l1}_[{l2}]_{self.suffix}_{l4}_{l3}'
                        path4=path3+'/'+folders_l4
                        self.create_folder_if_not_exist(path4)

        ########################## Level 5: files ###############################
                        file_folders=os.listdir(self.file_directory)
                        if l4 in file_folders:
                            for file in os.listdir(self.file_directory+'/'+l4):
                                file_dir=self.file_directory+'/'+l4+'/'+file
                                shutil.copy(file_dir,path4+'/')
                                filename,extension=tuple(file.split('.'))
                                new_file=f'{l1}_[{l2}]_{self.suffix}_{filename}_{l3}.{extension}'
                                os.rename(path4+'/'+file,path4+'/'+new_file)
        self.status=f'Proceso exitoso. {self.created_folders} carpetas creadas'


class tree_type_2(folder_tree):

    def __init__(self,root,level_file,suffix): #file_directory
        """
        expected_columns (dict) : dict with expected column by sheet and its types
        """
        expected_columns={'CLIENTES':{'GRUPO':str,'ALIAS':str,'AINI':int,'AFIN':int,'INCLUIR':str},'NIVEL':{'CARPETA':str}}
        super().__init__(root,level_file,expected_columns,suffix)
        if self.status!='OK': return
        self.check_year_boundries()
    
    def check_year_boundries(self):
        aini=self.sheets_dict['CLIENTES']['AINI']
        afin=self.sheets_dict['CLIENTES']['AFIN']
        checkaini=self.check_int_boundries(aini,2000,2100)
        checkafin=self.check_int_boundries(afin,2000,2100)
        checkboth=(afin>=aini).all()
        if checkaini and checkafin and checkboth:
            self.status='OK'
        elif not checkboth:
            self.status='AFIN siempre debe ser mayor que AINI'
        else:
            self.status='Revisar AINI o AFIN. Existen valores fuera del rango (2000, 2100)'

    def generate(self):
        """
        This function creates a folder tree inside the specified root, according to the level excel file.
        """
        ########################## Check if files are ok #################
        if self.status!='OK': return

        ########################## Initiate ########################## 
        path0=self.root
        self.created_folders=0
        df_clientes=self.sheets_dict['CLIENTES']
        df_carpetas=self.sheets_dict['NIVEL']

        ########################## Level 1 ###############################
        lvl1=df_carpetas['CARPETA']
        for l1 in lvl1:
            folders_l1=f'{self.suffix}_{l1}'
            path1=path0+'/'+folders_l1
            self.create_folder_if_not_exist(path1)
        
        ########################## Level 2 ###############################
            iniyear=df_clientes['AINI'].min()
            endyear=df_clientes['AFIN'].min()
            for y in range(iniyear,endyear+1):
                l2=y-2000
                folders_l2=f'{self.suffix}_{l1}_{l2}'
                path2=path1+'/'+folders_l2
                self.create_folder_if_not_exist(path2)
        
        ########################## Level 3 ###############################
        df_spec=df_clientes.dropna()
        for i in df_spec.index:
            grupo=df_spec.loc[i,'GRUPO']
            alias=df_spec.loc[i,'ALIAS']
            aini=df_spec.loc[i,'AINI']
            afin=df_spec.loc[i,'AFIN']
            incluir=df_spec.loc[i,'INCLUIR'].split(',')
            for y2 in range(aini,afin+1):
                for folder in incluir:
                    folder=folder.strip()
                    year=y2-2000
                    folders_l3=f'{grupo}_[{alias}]_{self.suffix}_{folder}_{year}'
                    path2=f'{self.root}/{self.suffix}_{folder}/{self.suffix}_{folder}_{year}'
                    path3=path2+'/'+folders_l3
                    if os.path.exists(path2):
                        self.create_folder_if_not_exist(path3)
        self.status=f'Proceso exitoso. {self.created_folders} carpetas creadas'
import os
import pandas as pd

class scontab:

    def __init__(self,root,level_file):
        self.root=root
        self.status='Inicializado'
        self.read_level_file(level_file)
        if self.status!='OK': return
        self.check_df_headers()
        if self.status!='OK': return
        self.check_df_types()

    def read_level_file(self,level_file):
        try:
            sheets_dict = pd.read_excel(level_file, sheet_name=None)
            self.df_clientes=sheets_dict['CLIENTES']
            self.df_generos=sheets_dict['GENEROS']
            self.status='OK'
        except:
            self.status='Archivo invalido: Revisar nombre de hojas'

    def check_df_headers(self):
        """
        Headers must be what is excpected
        """
        cli_cols=self.df_clientes.columns.to_list()==['GRUPO','ALIAS','AINI','AFIN']
        gen_cols=self.df_generos.columns.to_list()==['GENERO']
        if cli_cols and gen_cols:
            self.status='OK'
        elif cli_cols:
            self.status=f'Error en columnas de archivo de generos. Se esperaba \'GENERO\', pero contiene {self.df_generos.columns.to_list()}'
        elif gen_cols:
            self.status=f'Error en columnas de archivo de clientes. Se esperaba \'GRUPO\',\'ALIAS\',\'AINI\',\'AFIN\', pero contiene {self.df_clientes.columns.to_list()}'
        else:
            self.status='Error en nombre de columnas en ambas hojas.'

    def check_df_types(self):
        """
        Validate datatypes of input file.
        String field should be non empty.
        Numeric fields must be a number and it should be 2000<=x<2100.
        """
        non_empty=[self.df_clientes['GRUPO'],self.df_clientes['ALIAS'],self.df_generos['GENERO']]
        bounded_numeric=[self.df_clientes['AINI'],self.df_clientes['AFIN']]
        
         ########################## String variables ###############################
        for series in non_empty:
            check=series.apply(lambda x: x!='')
            if check.all():
               self.status='OK'
            else:
                self.status=f'Hay columnas con datos vacios. Revisar {series.name}'
                return

         ########################## Numeric variables ###############################
        for series in bounded_numeric:
            check_numeric=series.apply(lambda x: isinstance(x, (int,float)))
            if check_numeric.all():
                check_bounded=series.apply(lambda x: x>=2000 and x<2100) 
                if check_bounded.all():
                    self.status='OK'
                else:
                    self.status=f'Hay numeros fuera del rango aceptado. Revisar {series.name}'
                    return
            else:
                self.status=f'La columna {series.name} solo acepta datos numericos'
                return


    def create_folder_if_not_exist(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
            self.created_folders+=1

    def generate(self):
        """
        This function creates a folder tree inside the specified root, according to the level excel file.
        """
        ########################## Check if files are ok #################
        if self.status!='OK': return

        ########################## Initiate ########################## 
        path0=self.root
        self.created_folders=0

        ########################## Level 1 ###############################
        lvl1=self.df_clientes['GRUPO'].unique()
        for l1 in lvl1:
            folders_l1=f'{l1}_CON'
            path1=path0+'/'+folders_l1
            self.create_folder_if_not_exist(path1)
        
        ########################## Level 2 ###############################
            lvl2=self.df_clientes[self.df_clientes['GRUPO']==l1]['ALIAS']
            for l2 in lvl2:
                folders_l2=f'{l1}_[{l2}]_CON'
                path2=path1+'/'+folders_l2
                self.create_folder_if_not_exist(path2)
            
        ########################## Level 3 ###############################    
                iniyear=int(self.df_clientes[(self.df_clientes['GRUPO']==l1) & (self.df_clientes['ALIAS']==l2)]['AINI'].iloc[0])
                endyear=int(self.df_clientes[(self.df_clientes['GRUPO']==l1) & (self.df_clientes['ALIAS']==l2)]['AFIN'].iloc[0])
                for y in range(iniyear,endyear+1):
                    l3=y-2000
                    folders_l3=f'{l1}_[{l2}]_CON_{l3}'
                    path3=path2+'/'+folders_l3
                    self.create_folder_if_not_exist(path3)
        
        ########################## Level 4 ###############################
                    lvl4=self.df_generos['GENERO']
                    for l4 in lvl4:
                        folders_l4=f'{l1}_[{l2}]_CON_{l4}_{l3}'
                        path4=path3+'/'+folders_l4
                        self.create_folder_if_not_exist(path4)
        self.status=f'Proceso exitoso. {self.created_folders} carpetas creadas'
import os
import pandas as pd


def checkFolder(directory,file_dict):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and not filename.startswith('.'):
            file_dict.append({'full_path':f,'path':directory,'filename':filename})
        elif os.path.isdir(f):
            checkFolder(f,file_dict)

def create_extract_file(output_file,directory):
    info=[]
    checkFolder(directory,info)
    out_df=pd.DataFrame(info)
    out_df.to_excel(output_file, index=False)

def rename_files(filepath):
    files_not_found=[]
    df=pd.read_excel(filepath)
    for i in range(len(df)):
        new_path=df.loc[i,'new_path']
        if new_path!='' and not pd.isna(new_path):
            full_path=df.loc[i,'full_path']
            try:
                os.rename(full_path,new_path)
            except:
                files_not_found.append(full_path)
    if len(files_not_found)>0:
        logs=pd.DataFrame(files_not_found,columns=['files_not_found'])
        logs.to_excel('logs_files_not_found.xlsx')

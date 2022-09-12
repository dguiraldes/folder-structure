import os
import shutil
import pandas as pd


def checkFolder(directory,file_dict):
    """
    Recursive function that reads all files within a directory and fills up a list of dict containing all files and their paths.
    This function excludes files that start with a "."
    """
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and not filename.startswith('.'):
            file_dict.append({'full_path':f,'path':directory,'filename':filename,'full_path_len':len(f)})
        elif os.path.isdir(f):
            checkFolder(f,file_dict)

def create_extract_file(output_file,directory):
    """
    Function that read all files in a directory, format them as a pandas Dataframe and stores it in an Excel file

    Return length of output excel
    """
    info=[]
    checkFolder(directory,info)
    out_df=pd.DataFrame(info)
    out_df['relative_path']=out_df['full_path'].str.replace(directory,'',regex=False)
    out_df['relative_path_len']=out_df['relative_path'].apply(lambda x: len(x))
    out_df['new_file']=''
    out_df['new_path']=''
    out_df.to_excel(output_file, index=False)
    return(len(out_df))

    


def rename_files(filepath,copy_mode=False):
    """"
    Function that receives the path to an excel file containing the path of to an excel tat must have two columns: full_path and new_path, 
    and rename the files or copy them according the selected mode.

    Returns dict with lengths to show results
    """
    files_not_found=[] #List of paths included in full_path column, but not found when trying to rename/copy
    q_files=0
    df=pd.read_excel(filepath)
    for i in range(len(df)):
        new_path=df.loc[i,'new_path']
        if new_path!='' and not pd.isna(new_path):
            full_path=df.loc[i,'full_path']
            try:
                if copy_mode:
                    shutil.copy(full_path,new_path)
                else:
                    os.rename(full_path,new_path)
                q_files+=1
            except FileNotFoundError:
                files_not_found.append(full_path)
            except shutil.SameFileError:
                pass 
    if len(files_not_found)>0:
        logs=pd.DataFrame(files_not_found,columns=['files_not_found'])
        logs.to_excel('logs_files_not_found.xlsx')
    
    return ({'files_not_found':len(files_not_found),'processed_files':q_files})
    
    


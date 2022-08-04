import os


def checkFolder(directory,file_dict):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            file_dict.append({'full_path':f,'path':directory,'filename':filename})
        elif os.path.isdir(f):
            checkFolder(f,file_dict)

def create_extract_file(output_file):
    print(output_file)

def rename_files(filepath):
    print(filepath)
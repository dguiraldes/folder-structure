import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
from tree_types import scontab_tree
import os


class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()
        
    def configure_gui(self):
        self.master.title("Creador de carpetas")
        # self.master.geometry("500x500")

    def create_widgets(self):
        self.choose_folder_var=tk.StringVar()
        self.label_button_row(self.choose_folder_var,self.open_dir,"Seleccionar carpeta matriz",0)
        self.choose_file_var=tk.StringVar()
        self.label_button_row(self.choose_file_var,self.open_file,"Seleccionar archivo de estructura",1)
        self.tree_type(2)
        self.generate_tree_button(3)
        
    def label_button_row(self,var,cmd,text="",order=0):
        var.set("")
        id_label=tk.Label(self.master, textvariable=var)
        btn_open = tk.Button(self.master, text=text, command=cmd)

        id_label.grid(row=order, column=1, sticky="ns", padx=5, pady=5)
        btn_open.grid(row=order, column=0, sticky="ns", padx=5, pady=5)

    def tree_type(self,order):
        id_label=tk.Label(self.master, text="Tipo de estructura")
        OPTIONS=['SCONTAB']
        self.tree_type_var=tk.StringVar()
        opts=tk.OptionMenu(self.master, self.tree_type_var, *OPTIONS)

        id_label.grid(row=order, column=0, sticky="ns", padx=5, pady=5)
        opts.grid(row=order, column=1, sticky="ns", padx=5, pady=5)

    def generate_tree_button(self,order):
        btn=tk.Button(self.master, text='Generar carpetas', command=self.generate_tree)
        btn.grid(row=order, column=0, sticky="ns", padx=5, pady=5)
        



    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Excel Files", "*.xlsx"), ("Excel Files", "*.xls")]
        )
        if not filepath:
            return
        else:
            self.choose_file_var.set(filepath)
    
    def open_dir(self):
        """Open a directory"""
        rootpath = askdirectory(initialdir=os.curdir)
        if not rootpath:
            return
        else:
            self.choose_folder_var.set(rootpath)

    def generate_tree(self):
        root=self.choose_folder_var.get()
        level_file=self.choose_file_var.get()
        tree_type=self.tree_type_var.get()
        if root and level_file and tree_type:
            if tree_type=='SCONTAB':
                print(root)
                print(level_file)
                scontab_tree(root,level_file)
        else:
            print('shet')

    

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()
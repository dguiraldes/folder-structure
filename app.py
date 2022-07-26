import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
from tree_types import scontab
import os


class MainApplication(tk.Frame):

########################## Main structure
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
        
        self.tree_type_var=tk.StringVar()
        self.tree_type(self.tree_type_var,2)

        self.process_status_var=tk.StringVar()
        self.label_button_row(self.process_status_var,self.generate_tree,"Generar carpetas",order=3,btn_bg='blue',btn_fg='white')


####################### Place buttons and labels

    def label_button_row(self,var,cmd,text="",order=0, btn_bg='grey', btn_fg='black'):
        var.set("")
        id_label=tk.Label(self.master, textvariable=var)
        btn_open = tk.Button(self.master, text=text, bg=btn_bg, fg=btn_fg, command=cmd)

        id_label.grid(row=order, column=1, sticky="ns", padx=5, pady=5)
        btn_open.grid(row=order, column=0, sticky="ns", padx=5, pady=5)

    def tree_type(self,var,order):
        id_label=tk.Label(self.master, text="Tipo de estructura")
        OPTIONS=['SCONTAB']

        var.set('SCONTAB')
        opts=tk.OptionMenu(self.master, var, *OPTIONS)

        id_label.grid(row=order, column=0, sticky="ns", padx=5, pady=5)
        opts.grid(row=order, column=1, sticky="ns", padx=5, pady=5)
        
####################### Button methods

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
        self.process_status_var.set('')
        root=self.choose_folder_var.get()
        level_file=self.choose_file_var.get()
        tree_type=self.tree_type_var.get()
        if root and level_file and tree_type:
            if tree_type=='SCONTAB':
                tree=scontab(root,level_file)
                tree.generate()
                self.process_status_var.set(tree.status)
        else:
            self.process_status_var.set('Faltan campos por seleccionar')

    

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()
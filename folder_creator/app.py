import tkinter as tk
from tkinter.filedialog import askopenfilename,askdirectory
from tree_types import tree_type_1,tree_type_2
import os, sys


class MainApplication(tk.Frame):

########################## Main structure
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

        # Embedded app icon
        datafile = "icon.ico" 
        if not hasattr(sys, "frozen"):
            datafile = os.path.join(os.path.dirname(__file__), datafile) 
        else:  
            datafile = os.path.join(sys.prefix, datafile)
        self.master.iconbitmap(default=datafile)
        
    def configure_gui(self):
        self.master.title("Creador de carpetas")
        # self.master.geometry("500x500")

    def create_widgets(self):
        self.choose_folder_var=tk.StringVar()
        self.label_button_row(self.choose_folder_var,self.open_root_dir,"Seleccionar carpeta raiz",0)
        
        self.choose_file_var=tk.StringVar()
        self.label_button_row(self.choose_file_var,self.open_file,"Seleccionar archivo de estructura",1)
        
        self.tree_type_var=tk.StringVar()
        self.tree_type(self.tree_type_var,2)

        self.choose_file_directory_var=tk.StringVar()
        self.choose_file_directory_button=tk.Button(self.master, text="Seleccionar carpeta modelo",command=self.open_file_dir)
        self.label_state_button_row(self.choose_file_directory_var,self.choose_file_directory_button,order=3)

        self.suffix_var=tk.StringVar()
        self.suffix(self.suffix_var,4)

        self.process_status_var=tk.StringVar()
        self.label_button_row(self.process_status_var,self.generate_tree,"Generar carpetas",order=5,btn_bg='blue',btn_fg='white')


####################### Place buttons and labels

    def label_button_row(self,var,cmd,text="",order=0, btn_bg='#f0f0f0', btn_fg='black'):
        var.set("")
        id_label=tk.Label(self.master, textvariable=var)
        btn_open = tk.Button(self.master, text=text, bg=btn_bg, fg=btn_fg, command=cmd)

        id_label.grid(row=order, column=1, sticky="ns", padx=5, pady=5)
        btn_open.grid(row=order, column=0, sticky="ns", padx=5, pady=5)

    def label_state_button_row(self,var,btn,order=0):
        var.set("")
        id_label=tk.Label(self.master, textvariable=var)

        id_label.grid(row=order, column=1, sticky="ns", padx=5, pady=5)
        btn.grid(row=order, column=0, sticky="ns", padx=5, pady=5)


    def tree_type(self,var,order):
        id_label=tk.Label(self.master, text="Tipo de estructura")
        OPTIONS=['Por Grupo','Por Funcion']

        var.set('Por Grupo')
        opts=tk.OptionMenu(self.master, var, *OPTIONS, command=lambda _:self.changeState())

        id_label.grid(row=order, column=0, sticky="ns", padx=5, pady=5)
        opts.grid(row=order, column=1, sticky="ns", padx=5, pady=5)

    def suffix(self,var,order):
        id_label=tk.Label(self.master, text="Prefijo de carpetas")

        var.set('CON')
        opts=tk.Entry(self.master, textvariable=var)

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
    
    def open_root_dir(self):
        """Open a directory"""
        rootpath = askdirectory(initialdir=os.curdir)
        if not rootpath:
            return
        else:
            self.choose_folder_var.set(rootpath)

    def open_file_dir(self):
        """Open a directory"""
        rootpath = askdirectory(initialdir=os.curdir)
        if not rootpath:
            return
        else:
            self.choose_file_directory_var.set(rootpath)

    def changeState(self):
        pick = self.tree_type_var.get()
        if (pick == "Por Grupo"):
            self.choose_file_directory_var.set("")
            self.choose_file_directory_button['state'] = tk.ACTIVE #means active state
        else:
            self.choose_file_directory_var.set("No requiere carpeta modelo")
            self.choose_file_directory_button['state'] = tk.DISABLED #means disabled state

    def generate_tree(self):
        self.process_status_var.set('')
        root=self.choose_folder_var.get()
        level_file=self.choose_file_var.get()
        tree_type=self.tree_type_var.get()
        suffix=self.suffix_var.get()
        file_directory=self.choose_file_directory_var.get()
        if root and level_file and tree_type and suffix:
            try:
                if tree_type=='Por Grupo':
                    tree=tree_type_1(root,level_file,suffix,file_directory)
                elif tree_type=='Por Funcion':
                    tree=tree_type_2(root,level_file,suffix)
                tree.generate()
                self.process_status_var.set(tree.status)
            except Exception as e:
                self.process_status_var.set(f'Error inesperado: {e}')
        else:
            self.process_status_var.set('Faltan campos por seleccionar')

    

if __name__ == '__main__':
   root = tk.Tk()
   main_app =  MainApplication(root)
   root.mainloop()
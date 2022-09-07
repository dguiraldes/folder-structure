import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename,askdirectory
import os
from utils import create_extract_file,rename_files


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        self.title('Renombrador')
        #self.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)),"rename_icon.ico"))

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting of the different page layouts
        for F in (Home, FileExtractApp, RenameApp):

            frame = F(container, self)

            # initializing frame of that object from
            # Home, FileExtractApp, RenameApp respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(Home)

	# to display the current frame passed as
	# parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# first window frame Home
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text ="¿Qué quieres hacer?",font=("Verdana", 14, 'bold'))
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        button1 = ttk.Button(self, text ="Extraer archivos de carpeta",
        command = lambda : controller.show_frame(FileExtractApp))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)

        button2 = ttk.Button(self, text ="Renombrar archivos",
        command = lambda : controller.show_frame(RenameApp))
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		
class FileExtractApp(tk.Frame):
	
    def __init__(self, parent, controller):
        self.parent=parent
        self.controller=controller
        tk.Frame.__init__(self, parent)
        self.configure_gui()
        self.widgets()

    def configure_gui(self):
        label = ttk.Label(self, text ="Extraer archivos de carpeta", font=("Verdana", 14, 'bold'))
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        button1 = ttk.Button(self, text ="Menu", command = lambda : self.controller.show_frame(Home))
        button1.grid(row = 0, column = 0, padx = 10, pady = 10)
    
    def widgets(self):
        self.extraction_directory_var=tk.StringVar()
        self.extraction_directory_var.set("")
        extraction_directory_label=ttk.Label(self, textvariable=self.extraction_directory_var)
        extraction_directory_btn = ttk.Button(self, text="Seleccionar carpeta", command= lambda : self.openFolder(self.extraction_directory_var))

        extraction_directory_btn.grid(row=1, column=0, sticky="ns", padx=5, pady=5)
        extraction_directory_label.grid(row=1, column=1, sticky="ns", padx=5, pady=5)

        self.output_filename_var=tk.StringVar()
        self.output_filename_var.set('renombre')
        output_filename_entry=ttk.Entry(self, textvariable=self.output_filename_var)
        output_filename_label=ttk.Label(self,text='Nombre de archivo de salida')
        output_filename_suffix=ttk.Label(self,text='.xlsx')

        output_filename_entry.grid(row=2, column=1, sticky="ns", padx=5, pady=5)
        output_filename_label.grid(row=2, column=0, sticky="ns", padx=5, pady=5)
        output_filename_suffix.grid(row=2,column=2)

        extraction_process_button=ttk.Button(self, text="Extraer", command= lambda : self.extractFileNames(overwrite=False))
        extraction_process_button.grid(row=3, column=1, sticky="ns", padx=5, pady=5)

        self.status_var=tk.StringVar()
        self.status_var.set("")
        status_label=ttk.Label(self, textvariable=self.status_var)
        status_label.grid(row=4,column=1)

    
    def openFolder(self,var):
        """Open a directory"""
        rootpath = askdirectory(initialdir=os.curdir) #Here the the origin path is set
        if not rootpath:
            return
        else:
            var.set(rootpath)

    def open_popup(self):
        window = Popup(self)
        window.grab_set()


    def extractFileNames(self,overwrite):
        """
        Function called by "Extraer" button, used to extract information and generate output file
        """
        #Get values from entrys
        extraction_directory=self.extraction_directory_var.get()
        extraction_directory=os.path.normcase(extraction_directory)
        output_filename=self.output_filename_var.get()
        if extraction_directory and output_filename:
            #Assign path of output file (at the same level of extracted info)
            path=os.path.split(extraction_directory)[0]
            output_file=os.path.join(path,output_filename+'.xlsx')
            #If file already exists open popup to check if overwrite 
            if overwrite or not os.path.exists(output_file):
                self.status_var.set("Creando archivo de extracción")
                try:
                    files=create_extract_file(output_file,extraction_directory)
                    self.status_var.set(f'Archivo de {files} filas creado.\n{output_file}')
                except Exception as e:
                    self.status_var.set(f'No se pudo ejecutar el proceso:\n{str(e)}')

            else:
                self.open_popup()


# third window frame RenameApp
class RenameApp(tk.Frame):

    def __init__(self, parent, controller):
        self.parent=parent
        self.controller=controller
        self.overwrite=False
        tk.Frame.__init__(self, parent)
        self.configure_gui()
        self.widgets()

    def configure_gui(self):
        label = ttk.Label(self, text ="Renombrador de archivos", font=("Verdana", 14, 'bold'))
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        button1 = ttk.Button(self, text ="Menu", command = lambda : self.controller.show_frame(Home))
        button1.grid(row = 0, column = 0, padx = 10, pady = 10)
    
    def widgets(self):
        self.rename_file_var=tk.StringVar()
        self.rename_file_var.set("")
        rename_file_label=ttk.Label(self, textvariable=self.rename_file_var)
        rename_file_btn = ttk.Button(self, text="Seleccionar archivo", command= lambda : self.open_file(self.rename_file_var))

        rename_file_btn.grid(row=1, column=0, sticky="ns", padx=5, pady=5)
        rename_file_label.grid(row=1, column=1, sticky="ns", padx=5, pady=5)

        buttonFrame=tk.Frame(self)
        buttonFrame.grid(row=2,column=1)

        extraction_process_button=ttk.Button(buttonFrame, text="Renombrar", command= lambda : self.Rename(copy_mode=False))
        extraction_process_button.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        extraction_process_button=ttk.Button(buttonFrame, text="Copiar", command= lambda : self.Rename(copy_mode=True))
        extraction_process_button.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        self.status_var=tk.StringVar()
        self.status_var.set("")
        status_label=ttk.Label(self, textvariable=self.status_var)
        status_label.grid(row=3,column=1)


    def open_file(self,var):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Excel Files", "*.xlsx"), ("Excel Files", "*.xls")],initialdir=os.curdir)
        if not filepath:
            return
        else:
            var.set(filepath)


    def Rename(self,copy_mode):
        """
        Function to rename. Normcase is used in order to correctly format path independent from the OS
        """
        rename_file=self.rename_file_var.get()
        rename_file=os.path.normcase(rename_file)
        if rename_file:
            try:
                self.status_var.set('Procesando')
                results=rename_files(rename_file,copy_mode)
                pf=results['processed_files']
                nf=results['files_not_found']
                type= 'copiados' if copy_mode else 'renombrados'
                self.status_var.set(f'Listo!\nArchivos {type}: {pf}\nArchivos no encontrados: {nf}')
            except Exception as e:
                self.status_var.set(f'No se pudo ejecutar el proceso:\n{str(e)}')



class Popup(tk.Toplevel):
    """
    Popup opening from extractFilenames asking if overwriting file when it already exists
    """
    def __init__(self, parent):
        self.parent=parent
        super().__init__(parent)

        #self.geometry('300x100')
        self.title('Archivo ya existe')

        label = ttk.Label(self, text ="Este archivo ya existe,\n ¿quieres sobreescribirlo?")
        label.grid(row = 0, column = 0, padx = 10, pady = 10)

        buttonFrame=tk.Frame(self)
        buttonFrame.grid(row=1,column=0)

        accept_btn = ttk.Button(buttonFrame,
                    text='Aceptar',
                    command=self.accept)

        reject_btn= ttk.Button(buttonFrame,
                    text='Cancelar',
                    command=self.destroy)

        accept_btn.grid(row=0, column=0)
        reject_btn.grid(row=0, column=1)
    
    def accept(self):
        """
        If acceopt, call extract funcition with overwrite mode
        """
        self.parent.extractFileNames(overwrite=True)
        self.destroy()

# Driver Code
app = tkinterApp()
app.mainloop()

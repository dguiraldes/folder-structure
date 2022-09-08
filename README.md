# folder-structure

This project contains two apps developed for the company Vivas. Their goal was to save their files in a more structured way. The first app "folder_crator" is used to create a set of folders and subfolders according to the company's needs. Parameters can be configured using an Excel file. The second app "file_rename" is used to read files inside a selected folder, export their location to an Excel and assign a new path and name to the files. 


## Create app for windows (pyinstaller)


> :warning: Using pyinstaller with anaconda distribution will create a very large file. Instead create a small virtual env using only libraries needed. In this case, I created a requirements.txt file with the libraries used in each project. Here are the steps I follwed: https://stackoverflow.com/a/52272853,

To compile a python code with pyinstaller from scratch, activate a virtual environment with specific libraries used and then create the app with:

```
pyinstaller.exe app.py --onefile --icon icon.ico -n Creador -w 
```

If you already have a .spec file, to create exe file you should run:

```
pyinstaller.exe  Renombrador.spec
```


>Note for future Diego: Here's what you did to create virtual environment using python 3.9.13

```
$python -m venv C:\Users\Diego\vivas_pyinstall_env
$C:\Users\Diego\vivas_pyinstall_env\Scripts\activate
```
The requirements for this env are listed in **requiremnts.txt**.



## Code to embed icon in app
Solution by ALI3N (https://stackoverflow.com/a/41723750)

Follow these steps:

Edit your .spec file like this:
```
a = Analysis(....)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries + [('your.ico', 'path_to_your.ico', 'DATA')], 
          a.zipfiles,
          a.datas, 
          name=....
       )
```
Add this to your script:

```
datafile = "your.ico" 
if not hasattr(sys, "frozen"):
    datafile = os.path.join(os.path.dirname(__file__), datafile) 
else:  
    datafile = os.path.join(sys.prefix, datafile)
```

Use it this way:
```
root = tk.Tk()
root.iconbitmap(default=datafile)
```
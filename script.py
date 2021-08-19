import os
import PyPDF2
import pikepdf
import re

folder = input('Por favor ingrese la ruta: (por ejemplo: C:\OD\OneDrive\Consejo Superior de la Judicatura\Cuaderno Tribunal02 \n--> ')
# folder = r'C:\OD\OneDrive - Consejo Superior de la Judicatura\11 Dra Niño\Autos\ORD76001310500920200048401 - copia\Cuaderno Tribunal' 

# Aquí verifico si el pdf es un Oficio
def is_oficio_pdf(file):
    pdf = pikepdf.open(file)
    pdf.save('temp.pdf')

    file = open("temp.pdf", 'rb')

    pdfReader = PyPDF2.PdfFileReader(file)
    pages = pdfReader.numPages
    pdf_type = False
    for i in range(pages):
            pageObj = pdfReader.getPage(i)
            text = pageObj.extractText().split("  ")
            for i in range(len(text)):
                if text[i].split('\n').count('Oficio No.'):
                    pdf_type = True
    file.close()
    os.remove('temp.pdf')
    return pdf_type

# Aquí cuento cuántos PDF hay en la carpeta 
def pdf_files_counter(files):
    files_extensions = []           
    for file in files:
        file_extension = file.split('\\')[-1].split('.')[-1]
        files_extensions.append(file_extension)    
    return files_extensions.count('pdf')

# Aquí está la lógica que cambia los archivos de nombre
def change_filenames(folder, files):
    pdf_counter = pdf_files_counter(files)
    png_files_counter = 0

    for file in files:
        # Aquí busco la extensión para cada archivo que hay en la carpeta
        file_names = file.split('\\')[-1].split('.')[0]
        file_extension = file.split('\\')[-1].split('.')[-1]
        # Aquí extraigo el radicado del Folder contenedor
        upper_folder = folder.split('\\')[-2]
        radicate_serial = re.sub("[^0-9]","", upper_folder)[:23]
        # Valido que el radicado tenga 23 dígitos
        if len(radicate_serial) == 23:
            radicate_serial = radicate_serial[-14:]
            old_name = file
            new_name = ""
            # Aquí está la lógica para cuando el archivo es un Excel con macros
            if file_extension == 'xlsm':
                new_name = folder + r"\00IndiceElectronico" + radicate_serial + ".xlsm"        
                os.rename(old_name,new_name)
            # Aquí está la lógica para cuando el archivo es un PDF
            elif file_extension == 'pdf':
                # Si el pdf es un Oficio
                if is_oficio_pdf(file):
                    new_name = folder + r"\01Oficio"+"Remite" + radicate_serial + ".pdf"
                # Si el pdf no es un Oficio
                else:
                    new_name = folder + r"\02Ficha"+"Remite" + radicate_serial + ".pdf" 
                os.rename(old_name,new_name)
            # Aquí está la lógica para cuando el archivo es un PNG
            elif file_extension == 'png':
                new_name=folder + r"\0" + str(pdf_counter + png_files_counter + 1) + "ActaReparto" + radicate_serial + '.png'
                png_files_counter += 1
                os.rename(old_name,new_name)
        else:
            print('Algo pasa con el nombre de la carpeta de radicados. No tiene 23 números. Por favor verifique. \n Ningún archivo ha sido modificado')
        print(file_names)
    print('\nLos archivos fueron renombrados correctamente\n')

try:
    files = [ f.path for f in os.scandir(folder) if not f.is_dir() ]
    change_filenames(folder, files)

except:
    print('ERROR!!! ¿El direcorio "' + folder + '" existe?')






import os
import PyPDF2
import pikepdf

base_path = 'C:/OD/OneDrive - Consejo Superior de la Judicatura/'
rad_number = input('Ingrese el número de radicado que desea renombrar: ')
# rad_number = '12345678901234567890abc'

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

def change_filenames(folder, files):
    folder_extensions = []           
    def pdf_counter(files):
        for file in files:
            file_extension = file.split('\\')[-1].split('.')[-1]
            folder_extensions.append(file_extension)    
        return folder_extensions.count('pdf')

    pdf_counter = pdf_counter(files)
    actas_counter = 0

    for file in files:
        file_extension = file.split('\\')[-1].split('.')[-1]
        radicate_serial = folder.split('/')[-1][-14:]
        old_name = file
        new_name = ""
        if file_extension == 'xlsm':
            new_name = folder + r"\00IndiceElectronico" + radicate_serial + ".xlsm"        
            os.rename(old_name,new_name)
        elif file_extension == 'pdf':
            if is_oficio_pdf(file):
                new_name = folder + r"\01Oficio"+"Remite" + radicate_serial + ".pdf"
            else:
                new_name = folder + r"\02Ficha"+"Remite" + radicate_serial + ".pdf" 
            os.rename(old_name,new_name)
        elif file_extension == 'png':
            new_name=folder + r"\0" + str(pdf_counter + actas_counter + 1) + "ActaReparto" + radicate_serial + '.png'
            actas_counter += 1
            os.rename(old_name,new_name)

try:
    subfolders = [ f.path for f in os.scandir(base_path) if f.is_dir() ]
    for folder in subfolders:
        if folder.split('/')[-1] == rad_number: 
            rad_subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
            active_subfolder = ""
            for rad_subfolder in rad_subfolders:
                if rad_subfolder.split('\\')[-1][:17] == "Cuaderno Tribunal":
                    active_subfolder = rad_subfolder.split('\\')[-1]
            active_subfolder = folder + '/' + active_subfolder
            files = [ f.path for f in os.scandir(active_subfolder) if not f.is_dir() ]
            change_filenames(active_subfolder, files)
            print('Los archivos fueron renombrados correctamente')
except:
    print('ERROR!!! ¿El direcorio "' + base_path + '" existe?')






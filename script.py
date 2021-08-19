import os
import PyPDF2
import pikepdf

folder = input('Por favor ingrese la ruta: (por ejemplo: C:\OD\OneDrive\Consejo Superior de la Judicatura\Cuaderno Tribunal02 \n--> ')

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
    files_extensions = []           
    def pdf_counter(files):
        for file in files:
            file_extension = file.split('\\')[-1].split('.')[-1]
            files_extensions.append(file_extension)    
        return files_extensions.count('pdf')

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

    print('Los archivos fueron renombrados correctamente')

try:
    files = [ f.path for f in os.scandir(folder) if not f.is_dir() ]
    change_filenames(folder, files)

except:
    print('ERROR!!! ¿El direcorio "' + folder + '" existe?')






import sys, io

buffer = io.StringIO()
sys.stdout = sys.stderr = buffer

import os
import eel
import wx
import fitz
import time
import psutil
from pathlib import Path

from docx2pdf import convert

import shutil

eel.init("web")

Path(os.path.abspath("./Images")).mkdir(parents=True, exist_ok=True)
output_directory = (os.path.abspath("./Images"))

eel.dirName({'name': output_directory})
selected_files = []  # Store selected file paths here

@eel.expose
def select_directory():
    global output_directory
    app = wx.App(None)
    with wx.DirDialog(None, "Select a directory", style=wx.DD_DEFAULT_STYLE) as dirDialog:

        if dirDialog.ShowModal() == wx.ID_CANCEL:
            return None

        output_directory = dirDialog.GetPath()
        eel.dirName({'name': output_directory})

        return output_directory


@eel.expose
def pythonFunction():
    app = wx.App(None)
    wildcard = "Document files (*.pdf;*.docx)|*.pdf;*.docx"
    style = wx.FD_OPEN | wx.STAY_ON_TOP | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE  
    dialog = wx.FileDialog(None, "PDF to Image Converter", wildcard=wildcard, style=style)

    if dialog.ShowModal() == wx.ID_OK:
        global selected_files
        selected_files = dialog.GetPaths() 
    else:
        selected_files = []

    dialog.Destroy()

    eel.updateFileCount({'count': len(selected_files)})
    return selected_files


@eel.expose
def convert_selected_files():
    global selected_files
    temp_folder = "temp"

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    pdf_files = []

    total_files = len(selected_files)

    for index, path in enumerate(selected_files):
        try:
            file_extension = os.path.splitext(path)[1].lower()

            if file_extension == ".pdf":
                pdf_files.append(path)

            elif file_extension == ".docx":
                temp_file_path = os.path.join(temp_folder, os.path.basename(path))
                shutil.copy2(path, temp_file_path)
            else:
                print(f"Unsupported file type: {path}")

        except Exception as e:
            print(f"Error processing file {path}: {str(e)}")

    convert(temp_folder)
    pdf_files.extend(get_all_pdf_files(temp_folder))
    move_pdfs_to_original_folder(pdf_files)


def get_all_pdf_files(folder):
    # Get a list of all PDF files in the specified folder
    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    return [os.path.join(folder, pdf_file) for pdf_file in pdf_files]


def move_pdfs_to_original_folder(pdf_files):
    total_files = len(pdf_files)

    for index, pdf_path in enumerate(pdf_files, start=1):
        original_folder = os.path.dirname(pdf_path)
        destination_path = os.path.join(original_folder, os.path.basename(pdf_path))
        shutil.move(pdf_path, destination_path)

        progress(index, total_files)  

        update_file_path_for_image(destination_path)

    print("Moved and updated paths for PDF files")
    try:
        shutil.rmtree('temp')
    except Exception as e:
        print(f'Failed to delete directory: {e}')


@eel.expose
def update_file_path_for_image(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image = page.get_pixmap(dpi=(300))

            output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_number + 1}.png")
            image.save(output_path, "png")

        pdf_document.close()
    except Exception as e:
        print(f"Error converting image for file {pdf_path}: {str(e)}")


def sys_usage():
    cpu_usage = psutil.cpu_percent()  
    ram_usage = str(round((psutil.Process().memory_info().rss / psutil.virtual_memory().total) * 100 , 2))

    return (cpu_usage , ram_usage)


@eel.expose
def progress(count, total):
    cpu_usage, ram_usage = sys_usage()

    bar_len = 6
    filled_len = int(round(bar_len * count / float(total)))
    bar = '◼' * filled_len + '◻' * (bar_len - filled_len)

    eel.progress({'loadin': ('[%s]\r' % (bar)), 'cpu': f"{cpu_usage}", 'ram': f"{ram_usage}"})
    if count == total:
        time.sleep(3)
        eel.progress({'loadin': "", 'cpu': " NaN ", 'ram': " NaN "})

eel.start("index.html", size=(1200, 750), port=8000)
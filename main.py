import sys, io

#buffer = io.StringIO()
#sys.stdout = sys.stderr = buffer
import os
import eel
import wx
import fitz
import time
import psutil
from pathlib import Path


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
    wildcard = "Document files|*.pdf;"
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
    total_files = len(selected_files)

    for index, path in enumerate(selected_files):
        try:
            convert_image(path)
            progress(index + 1, total_files)
        except Exception as e:
            print(f"Error processing file {path}: {str(e)}")

@eel.expose
def convert_image(pdf_path):
    path_split = os.path.split(pdf_path)

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

    eel.progress({'loadin': ('[%s]\r' % (bar)),  'cpu':(f"{cpu_usage}"),  'ram': f"{ram_usage}"})
    if count == total:
        time.sleep(3)
        eel.progress({'loadin':"",  'cpu':" NaN ",  'ram':" NaN "  })

eel.start("index.html", size=(1200, 750), port=8000)

import os
from pathlib import Path
from PyPDF2 import PdfMerger


pdf_folder = input("Enter the folder path where the PDF files are located: ")

if not os.path.exists(pdf_folder):
    print("Folder does not exist. Please provide a valid folder path.")
    exit()

output_file_name = input("Enter the name of the merged PDF file (without extension): ")
output_file_path = f"{output_file_name}.pdf"

# Sorting files based on modification time
paths = sorted(Path(pdf_folder).iterdir(), key=os.path.getmtime)
paths_in_string = [str(path) for path in paths]


merger = PdfMerger()

for pdf_file in paths_in_string:
    merger.append(pdf_file)

output_path = os.path.join(os.getcwd(), output_file_path)
merger.write(output_path)

merger.close()

print(f"Merged PDF saved as {output_path}")

import pandas as pd
import os
import html
import re
import io
import xlsxwriter
import shutil
from pathlib import Path
from zipfile import ZipFile

def process_csv_file(file_path, output_folder):
    home = Path.home()

    # Create output directories if they don't exist
    resultExcelFilePath = os.path.join(output_folder, "ResultExcelFile.xlsx")
    data_folder = os.path.join(output_folder, 'Data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Read CSV file
    cvsDataframe = pd.read_csv(file_path)

    # Create Excel file from CSV
    with pd.ExcelWriter(resultExcelFilePath, engine='xlsxwriter') as writer:
        cvsDataframe.to_excel(writer, sheet_name='Sheet1')

    # Simulate article creation process
    for index, row in cvsDataframe.iterrows():
        folder_name = f"article_{index+1}"
        folder_path = os.path.join(data_folder, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Example of generating HTML content for each article
        question_html_path = os.path.join(folder_path, "Question.html")
        with io.open(question_html_path, "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>{html.escape(str(row['Front End Title']))}</h1></body></html>")

        answer_html_path = os.path.join(folder_path, "Answer.html")
        with io.open(answer_html_path, "w", encoding="utf-8") as f:
            f.write(f"<html><body>{html.escape(str(row['Content']))}</body></html>")

    # Create the zip file of all the generated content
    zip_file_path = os.path.join(output_folder, 'processed_output.zip')
    with ZipFile(zip_file_path, 'w') as zipf:
        # Add Excel file to the zip
        zipf.write(resultExcelFilePath, arcname="ResultExcelFile.xlsx")
        
        # Add each article folder and its contents to the zip
        for root, dirs, files in os.walk(data_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_folder)
                zipf.write(file_path, arcname=arcname)

    return os.path.basename(zip_file_path)
import spacy
from zipfile import ZipFile
import os
import pandas as pd
import PyPDF2
import docx2txt
import re


# accumulation of helper methods
class Tutor:  # should turn into a protocol rather than a class
    # english dictionary used
    nlp = spacy.load('en_core_web_sm')

    @staticmethod
    def extract_pdf_text(pdf_file):
        f = open(pdf_file, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(f)
        result_file = open(f"{pdf_file.replace('.pdf', '.txt')}", 'w+')
        for index in range(pdf_reader.numPages):
            page = pdf_reader.getPage(index)
            result_file.write(page.extractText())
        f.close()

    @staticmethod
    def format_zip(file):
        zp = ZipFile(file, 'r')
        zp.extractall(os.getcwd())
        nl = zp.namelist()
        if '__MACOSX/' in nl:
            nl.remove('__MACOSX/')
        return nl

    # files not accepted: xml, html, images: could also be used to download any file on a computer: .conf, .md, etc
    @staticmethod
    def retrieve(filepath, file_type):
        accepted_files = {
            'txt': lambda file: open(f'{file}', 'r+').read(),
            'csv': lambda file: pd.read_csv(f'{filepath}'),
            'xlsx': lambda file: pd.read_excel(f'{filepath}'),
            'json': lambda file: pd.read_json(f'{filepath}'),
            'hdf': lambda file: pd.read_hdf(f'{filepath}'),
            'pdf': lambda file: Tutor.extract_pdf_text(filepath),
            'tsv': lambda file: pd.read_csv(f'{filepath}'),
            'docx': lambda file: docx2txt.process(f'{filepath}')
        }
        return accepted_files[file_type]

    @staticmethod
    def move_files(topic, repository):
        for file in topic.files:
            os.rename(f'{file}', f'{repository}/{file}')

    # text_gen helper method 1
    @staticmethod
    def generic_file_extraction(filepaths):
        file_list = []
        for file in filepaths:
            file_type = file.split('.')[1]
            if file_type == 'zip':
                namelist = Tutor.format_zip(file)
                for name in namelist:
                    file_list.append(name)
            else: file_list.append(Tutor.retrieve(file, file_type))
        return file_list

    # make a directory and change into it
    @staticmethod
    def mcdir(filepath):
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        os.chdir(filepath)


    @staticmethod
    def chback():
        os.chdir('..')

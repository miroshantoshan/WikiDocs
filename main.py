import os
from pathlib import Path
from time import sleep
import re
import textwrap

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from utils import set_styles, download_picture, clear_dir,clearing_tags, create_document_folder, create_pictures_folder
from config import user_agent,picture_folder_path,document_path,document_folder_path


load_dotenv()

url = f''

create_pictures_folder(picture_folder_path)
create_document_folder(document_folder_path)

headers = user_agent

response = requests.get(url,verify=False, headers=headers)
response.raise_for_status()  

soup = BeautifulSoup(response.text, features='html.parser')

header = soup.find('h1', class_='firstHeading mw-first-heading')

content = soup.find('div', class_='mw-content-ltr mw-parser-output')

tags = content.find_all(['p','h2','img'])


doc = Document()

set_styles(doc,'Times New Roman',14)

head = doc.add_heading(header.text)
head.alignment = WD_ALIGN_PARAGRAPH.CENTER


needed_tags = clearing_tags(tags)

for index,tag in enumerate(needed_tags):

    if "</p>" in str(tag):

        match = re.sub(r"\[\w*\]","", tag.text)
        paragraphs = doc.add_paragraph(match)
        paragraphs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if "<img" in str(tag):
        link_photo = f"https:{tag['src']}"
        picture_name = f"image{index}"
        path = Path(picture_folder_path, f"{picture_name}.png")

        download_picture(link_photo,path,headers)
        
        doc.add_picture(f"{picture_folder_path}/{picture_name}.png")
        picture_paragraph = doc.paragraphs[-1]
        picture_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if "<h2" in str(tag):
        head2 = doc.add_heading(tag.text, level=2)
        head2.alignment = WD_ALIGN_PARAGRAPH.CENTER


doc.save(document_path)

clear_dir(picture_folder_path)

"*th*r*"


import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os
from dotenv import load_dotenv
from time import sleep
import textwrap
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
load_dotenv()




def set_styles(doc,font_name,font_size):
    style = doc.styles['Normal']
    style.font.name = font_name
    style.font.size = Pt(font_size)


def download_picture(link_photo,path,headers):
    response = requests.get(link_photo,verify=False, headers=headers)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)

def clear_dir(dir):
  for f in os.listdir(dir):
      os.remove(os.path.join(dir, f))



folder_path = ("./photos/")

url = 'https://ru.wikipedia.org/wiki/Вики'

headers = {'User-Agent' : 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; UP Vision Build/KOT49H)'}

response = requests.get(url,verify=False, headers=headers)
response.raise_for_status()  

soup = BeautifulSoup(response.text, features='html.parser')

header = soup.find('h1', class_='firstHeading mw-first-heading')

content = soup.find('div', class_='mw-content-ltr mw-parser-output')

tags = content.find_all(['p','h2','img'])

picture_folder_path = "./photos"

doc = Document()

set_styles(doc,'Times New Roman',14)

head = doc.add_heading(header.text)
head.alignment = WD_ALIGN_PARAGRAPH.CENTER

tags.reverse()

for index,tag in enumerate(tags):
    if "</p>" in str(tag):
        number = index
        break

needed_tags = tags[index:]

needed_tags.reverse()


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


doc.save('./documents/document.docx')

clear_dir(folder_path)


















"*th*r*"
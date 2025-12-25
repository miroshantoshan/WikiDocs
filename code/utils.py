
import os
import requests
from docx.shared import Pt
from config import picture_folder_path,document_folder_path



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

def clearing_tags(tags):
    tags.reverse()

    for index,tag in enumerate(tags):
        if "</p>" in str(tag):
            number = index
            break

    needed_tags = tags[index:]

    needed_tags.reverse()
    return needed_tags

def create_pictures_folder(picture_folder_path):
    os.makedirs(picture_folder_path, exist_ok=True)

def create_document_folder(document_folder_path):
    os.makedirs(document_folder_path, exist_ok=True)


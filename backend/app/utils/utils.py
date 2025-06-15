from fastapi import UploadFile
import shutil
import os
import json
from .paths import path_to_artifact, path_to_artifact_images, path_to_artifact_RTIs
from urllib.parse import urljoin


def upload_files(dest: str, files: list[UploadFile]):
    for file in files:
        file_path = os.path.join(dest, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            print(f"Added: {file.filename}")


def get_artifact_preview(id, base_url=""):
    try:
        metadata_file = os.path.join(path_to_artifact(id), "metadata.json")
        with open(metadata_file, "r") as file:
            metadata = json.load(file)
    except:
        metadata = {}
    
    # get a thumbnail from rti or images
    try:
        RTIs_dir = path_to_artifact_RTIs(id)
        first_RTI_id = os.listdir(RTIs_dir)[0]
        thumbnail_file = os.path.join(RTIs_dir, first_RTI_id, "thumbnail.jpg")
        if not os.path.isfile(thumbnail_file):
            raise Exception()
    except:
        try:
            images_dir = path_to_artifact_images(id)
            first_image_id = os.listdir(images_dir)[0]
            thumbnail_file = os.path.join(images_dir, first_image_id)
            if not os.path.isfile(thumbnail_file):
                raise Exception()
        except:
            thumbnail_file = ""
    
    return {
        "id": id,
        "title": metadata.get('title'),
        "description": metadata.get('description'),
        "date": metadata.get('date'),
        "thumbnail": urljoin(base_url, thumbnail_file),
    }

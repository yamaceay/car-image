import requests
import json
from tqdm import tqdm
from PIL import Image
import io
import os

with open("src_list.json", "r") as file:
    jsonified = file.read()
    datas = json.loads(jsonified)

for company in datas[1:]:
    links = company["links"]
    name = company["name"]
    link_names = [f"{name}_{i:03d}" for i in range(len(links))]
    for i in tqdm(range(len(links))):
        link = links[i]
        link_name = link_names[i]
        img_content = requests.get(link).content
        img_file = io.BytesIO(img_content)
        image = Image.open(img_file).convert("RGB")
        with open(f"imgs/{name}/{link_name}.jpg", "w") as file:
            image.save(file, "JPEG")
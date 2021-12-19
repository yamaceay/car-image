import json

from tqdm import tqdm
import pandas as pd
import numpy as np
import time

from selenium import webdriver
driver = webdriver.Chrome(executable_path = "chromedriver.exe")

df = pd.read_csv("companies.csv")

home = "https://images.google.com/"

length = len(df["name"])
indexes = np.random.permutation(length)
limit = 200

datas = []
for index in tqdm(range(length)):
    i = indexes[index]
    name = df["name"].iloc[i]
    driver.get(home)
    input_box = driver.find_element_by_css_selector("div > div > input")
    input_box.send_keys(name)
    input_box.submit()
    length = 0
    while (length < limit):
        elems = driver.find_elements_by_css_selector("#islrg > div.islrc > div")
        length = len(elems)
        print(length)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
    links = [elem.find_element_by_css_selector("a > div > img").get_attribute("src") for elem in elems]
    links = [link for link in links if link is not None]
    links = [link for link in links if len(link) <= 500]
    print(f"Done: {len(links)} links!")
    data = {"name": name, "links": links}
    datas.append(data)

with open("src_list.json", "w") as file:
    jsonified = json.dumps(datas, indent=4)
    file.write(jsonified)

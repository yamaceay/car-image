from selenium import webdriver
import json
import pandas as pd
import re
driver = webdriver.Chrome(executable_path = "chromedriver.exe")

driver.get("https://www.carlogos.org/popular-car-brands/")

list_elems = driver.find_elements_by_css_selector("body > div.main > div.main-l > div.custom-list > ul > li")

data = {col: [] for col in ["rank", "logo_link", "origin", "name", "segment"]}

for elem in list_elems:
    info_elems = elem.find_elements_by_css_selector("div")
    rank = info_elems[0].get_attribute("innerText")
    logo_link = info_elems[1].find_element_by_css_selector("a > img").get_attribute("src")

    more_data = info_elems[2].find_elements_by_css_selector("*")
    origin = more_data[0].get_attribute("innerText")
    name = more_data[1].get_attribute("innerText")

    raw_segment = info_elems[2].get_attribute("innerText")
    segment = re.sub(origin, "", raw_segment)
    segment = re.sub(name, "", segment)
    segment = re.sub("\n", "", segment)

    vals = {"rank": rank, "logo_link": logo_link, "origin": origin, "name": name, "segment": segment}
    for col in vals.keys():
        val = vals[col]
        data[col].append(val)

df = pd.DataFrame(data)

df.set_index("rank").to_csv("companies.csv")

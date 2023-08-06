import requests, re
from bs4 import BeautifulSoup

IMSDB_URL = "https://imsdb.com/"
SCRIPTS_PATH = "scripts/"
GENRE_PATH = "genre/"

def get_urls(names):
    script_urls = list(map(lambda name: IMSDB_URL + SCRIPTS_PATH + "-".join(name.split()) + ".html", names))
    return script_urls

def get_names(genre):
    page = requests.get(IMSDB_URL + GENRE_PATH + genre.title())
    html = BeautifulSoup(page.content, "html.parser")
    script_elements = list(filter(lambda text: "Script" in str(text), html.find_all("p")))
    script_names = list(map(lambda element: element.find("a").text, script_elements))
    return script_names

def get_script(url):
    try:
        page = requests.get(url)
        html = BeautifulSoup(page.content, "html.parser")
        script = str(html.find("td", class_="scrtext").find("pre").find("pre"))
        script = re.sub("<b>", "", script)
        script = re.sub("</b>", "", script)
        script = re.sub("<pre>", "", script)
        script = re.sub("</pre>", "", script)
    except Exception as e:
        script = ""
        
    return script

def get_genres():
    page = requests.get(IMSDB_URL)
    html = BeautifulSoup(page.content, "html.parser")
    genre_elements = list(filter(lambda element: "/genre/" in str(element), html.find_all("a")))
    genres = list(map(lambda element: element.text, genre_elements))
    return genres



import re
import requests
import time
import urllib.parse
import warnings
from bs4 import BeautifulSoup
from clear import clear

CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RED = "\033[1;31m"

def pylotl(website, delay = 0):
    clear()
    
    website = website.rstrip("/")
    warnings.filterwarnings("ignore")
 
    banned = []
    visited = [website]

    start = True
    thread_list = []
    visit_now = -1
    while True:
        try:
            visit_now += 1
            visited = list(dict.fromkeys(visited[:]))
            print(f"{CYAN}visiting: {GREEN}{visited[visit_now]}", flush = True)
            time.sleep(delay)
            try:
                my_session = requests.Session() 
                my_request = my_session.get(visited[visit_now], verify = False, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}, timeout = 10)
                if my_request.status_code == 200:
                    data = my_request.text

            except:
                pass

            if data:
                links = []
               
                soup = BeautifulSoup(data, "html.parser")

                try:
                    new_links = soup.find_all("a")
                    for link in new_links:
                        if link.get("href") is not None:
                            links.append(link.get("href"))

                except:
                    pass

                try:
                    soup.findAll("img")
                    images = soup.find_all("img")
                    for image in images:
                        if image["src"] is not None:
                            links.append(image["src"])

                except:
                    pass

                try:
                    new_links = soup.find_all("link")
                    for link in new_links:
                        if link.get("href") is not None:
                            links.append(link.get("href"))
                       
                        if link.get("imagesrcset") is not None:
                            for i in link.get("imagesrcset").split(","):
                                links.append(i.strip())

                except:
                    pass
               
                links = list(dict.fromkeys(links[:]))
               
                for path in links:
                    if re.search("^[a-zA-Z0-9]", path.lstrip("/")) and not re.search("script|data:", path):
                        if path.startswith("/"):
                            visited.append(website + path)

                        elif path.startswith("http://") or path.startswith("https://"):
                            if urllib.parse.urlparse(website).netloc in urllib.parse.urlparse(path).netloc:
                                visited.append(path)

                        else:
                            visited.append(website + "/" + path)

                scripts = soup.find_all("script")
                for script in scripts:
                    if script.get("src") is not None:
                        path = script.get("src")
                        if re.search("^[a-zA-Z0-9]", path.lstrip("/")) and not re.search("script|data:", path):
                            if path.startswith("/"):
                                visited.append(website + path)
     
                            elif path.startswith("http://") or path.startswith("https://") or path.startswith("ftp://"):
                                visited.append(path)
     
                            else:
                                visited.append(website + "/" + path)
 
        except IndexError:
            break
 
        except:
            pass
 
    return visited

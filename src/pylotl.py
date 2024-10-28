import argparse
import re
import requests
import threading
import urllib.parse
import warnings
from bs4 import BeautifulSoup
from clear import clear

CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RED = "\033[1;31m"

def aggresive(host):
    global data

    try:
        my_session = requests.Session() 
        my_request = my_session.get(host, verify = False, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}, timeout = 10)
        if my_request.status_code == 200:
            data += f"{my_request.text}\n"

    except:
        pass

def pylotl():
    global data
    data = ""

    clear()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", type = str, required = True)
    args = parser.parse_args()
    website = args.host
    
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
            my_thread = threading.Thread(target=aggresive, args = (visited[visit_now],))
            thread_list.append(my_thread)
            my_thread.start()

            if start:
                my_thread.join()
                thread_list = []
                start = False

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

                data_list = []

            if len(thread_list) % 8 == 0:
                for thread in thread_list:
                    thread.join()

                thread_list = []
 
        except IndexError:
            break
 
        except:
            pass
 
    return visited

if __name__ == "__main__":
    pylotl()

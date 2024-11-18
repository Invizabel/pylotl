import argparse
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

fake_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "UPGRADE-INSECURE-REQUESTS": "1"}

def pylotl():
    clear()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", type = str, required = True)
    parser.add_argument("-crawl", type = int, required = True)
    parser.add_argument("-delay", type = float, required = False, default = 0)
    args = parser.parse_args()
    website = args.host

    my_session = requests.Session()
    website = website.rstrip("/")
    warnings.filterwarnings("ignore")
 
    banned = []
    visited = [website]

    for visit_now in range(args.crawl):
        try:
            visited = list(dict.fromkeys(visited[:]))
            print(f"{CYAN}visiting: {GREEN}{visited[visit_now]}", flush = True)

            time.sleep(args.delay)
            
            my_request = my_session.get(visited[visit_now], verify = False, headers = fake_headers, timeout = 10)
            data = my_request.text

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
 
    with open("links.txt", "a") as file:
        for link in visited:
            if urllib.parse.urlparse(website).netloc in link:
                file.write(f"{link}\n")

    print(f"{RED}DONE!")

if __name__ == "__main__":
    pylotl()

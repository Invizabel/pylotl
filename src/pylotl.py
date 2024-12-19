import datetime
import json
import os
import re
import threading
import time
import urllib.parse
import warnings
from bs4 import BeautifulSoup
from clear import clear
from flask import *
from selenium import webdriver

app = Flask(__name__)
queue = []
queue.append("https://www.example.com")

options = webdriver.FirefoxOptions()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)

def automatic_index():
    last_year = datetime.datetime.now().year
    while True:
        time.sleep(60)
        this_year = datetime.datetime.now().year
        if this_year != last_year:
            print("Starting automatic indexing!")
            index()
            print("Automatic indexing done!")

        last_year = datetime.datetime.now().year
        
def crawl(website):
    website = website.rstrip("/")
    warnings.filterwarnings("ignore")
 
    banned = []
    visited = [website]

    for visit_now in range(10000):
        try:
            visited = list(dict.fromkeys(visited[:]))
            print(f"crawling: {visited[visit_now]}")

            driver.get(visited[visit_now])
            data = driver.page_source
            if len(data) < 100000000:
                links = []
               
                soup = BeautifulSoup(data, "html.parser")

                try:
                    links = soup.find_all("a")
                    for link in links:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    div_container = soup.find("div")
                    links = div_container.find_all("a")
                    for link in links:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    link = soup.find("a", string="Click here")
                    if link:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    link = soup.find("a", string=re.compile("Click"))
                    if link:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    special_links = soup.find_all("a", attrs={'rel': 'nofollow'})
                    for link in special_links:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    nested_links = soup.find("div").find_all("a")
                    for link in nested_links:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    list_items = soup.find_all("li")
                    for item in list_items:
                        link = item.find("a")
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    table_rows = soup.find_all("tr")
                    for row in table_rows:
                        link = row.find("a")
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass

                try:
                    links = soup.find_all("link")
                    for link in links:
                        if "://" in urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")):
                            visited.append(urllib.parse.urljoin(urllib.parse.urlparse(visited[visit_now]).scheme + "://" + urllib.parse.urlparse(visited[visit_now]).netloc, link.get("href")))

                except:
                    pass
 
        except IndexError:
            break
 
        except:
            pass
    
    exists = []
    if os.path.exists("links.txt"):
        with open("links.txt", "r") as file:
            for line in file:
                new_line = line.rstrip("\n")
                exists.append(new_line)

    try:
        with open("links.txt", "a") as file:
            for link in visited:
                if urllib.parse.urlparse(website).netloc in link and link not in exists:
                    file.write(f"{link}\n")

    except:
        pass

    queue.remove(website)
    visited = []
                
def index():
    urls = []
    with open("links.txt", "r") as file:
        for line in file:
            new_line = line.rstrip("\n")
            urls.append(new_line.rstrip("/"))

    hits = {}

    count = -1
    while True:
        try:
            count += 1
            print(f"indexing: {urls[count]}")
            
            driver.get(urls[count])
            my_request = driver.page_source
            if len(my_request) < 100000000:
                soup = BeautifulSoup(my_request, "html.parser")
                [s.extract() for s in soup(["style", "script", "[document]", "head", "title"])]
                readable_text = soup.getText().split("\n")
                new_text = []
                for i in readable_text:
                    i = re.sub(r"\s+", " ", i)
                    if len(i) > 0 and i != " ":
                        new_text.append(i)

                new_text = list(dict.fromkeys(new_text[:]))
                new_text.sort()
                hits.update({urls[count]: new_text})

        except IndexError:
            break

        except:
            pass

    hits = json.dumps(hits, indent = 4, sort_keys = True)
    with open("index.json", "w") as file:
        file.write(hits)

def search(query):
    hits = []
    with open("index.json", "r") as file:
        json_data = json.loads(file.read())

    for key, value in json_data.items():
        for _ in value:
            if re.search(query, _):
                hits.append(key)

    hits = list(dict.fromkeys(hits[:]))
    hits.sort()

    if len(hits) > 0:
        return hits

    else:
        return None

@app.route("/crawl", methods=["GET", "POST"])
def crawl_html():
    global queue
    
    if os.path.exists("links.txt"):
        if request.method == "GET":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <form method="POST">
                      <label for="crawl">Crawl:</label><br>
                      <input type="text" id="crawl" name="crawl"><br>
                      <input type="submit" id="GO" name="GO" value="GO">
                      </strong><br><a href="/search">Search</a>
                      </form>
                      </body>
                      </html>
                    '''

            return  render_template_string(html)

        if request.method == "POST":
            urls = []
            with open("links.txt", "r") as file:
                for line in file:
                    new_line = line.rstrip("\n")
                    urls.append(new_line.rstrip("/"))

            for i in queue:
                if  i == request.form["crawl"].rstrip("/"):
                    html = '''<html>
                              <head>
                              <title>pylotl</title>
                              </head>
                              <body>
                              <form method="POST">
                              <label for="crawl">Crawl:</label><br>
                              <input type="text" id="crawl" name="crawl"><br>
                              <input type="submit" id="GO" name="GO" value="GO">''' + f'<br><strong>{request.form["crawl"]} is already queued</strong><br><a href="/search">Search</a></form></body></html>'''

                    return  render_template_string(html)

            if request.form["crawl"].rstrip("/") not in urls:
                queue.append(request.form["crawl"])
                crawl(request.form["crawl"])
                index()
                html = '''<html>
                          <head>
                          <title>pylotl</title>
                          </head>
                          <body>
                          <form method="POST">
                          <label for="crawl">Crawl:</label><br>
                          <input type="text" id="crawl" name="crawl"><br>
                              <input type="submit" id="GO" name="GO" value="GO">''' + f'<br><strong>Done crawling and indexing {request.form["crawl"]}</strong><br><a href="/search">Search</a></form></body></html>'''

                return  render_template_string(html)

            else:
                html = '''<html>
                          <head>
                          <title>pylotl</title>
                          </head>
                          <body>
                          <form method="POST">
                          <label for="crawl">Crawl:</label><br>
                          <input type="text" id="crawl" name="crawl"><br>
                          <input type="submit" id="GO" name="GO" value="GO">
                          </strong><br><a href="/search">Search</a></form></body></html>
                          </form>
                          <strong>We already have that indexed!</strong>
                          </body>
                          </html>'''
                
        return  render_template_string(html)

    else:
        crawl("https://www.example.com")
        index()
        html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <strong>We are currently setting up. Please try again!</strong>
                      </body>
                      </html>
                    '''

        return  render_template_string(html)

@app.route("/search", methods=["GET", "POST"])
def search_html():
    if os.path.exists("index.json"):
        if request.method == "GET":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <form method="POST">
                      <label for="query">Query:</label><br>
                      <input type="text" id="query" name="query"><br>
                      <input type="submit" id="GO" name="GO" value="GO">
                      </strong><br><a href="/crawl">Crawl</a>
                      </form>
                      </body>
                      </html>
                    '''
            
            return render_template_string(html)

        if request.method == "POST":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <form method="POST">
                      <label for="query">Query:</label><br>
                      <input type="text" id="query" name="query"><br>
                      <input type="submit" id="GO" name="GO" value="GO">
                      </strong><br><a href="/crawl">Crawl</a>
                      </form>
                      <br>
                    '''
            
            query = request.form["query"]
            hits = search(query)
            html += f'<strong>You searched for: {query}</strong><br>'
            if hits is not None:
                for hit in hits:
                    html += f'<a href="{hit}">{hit}</a><br>'

                html += '''</body>
                           </html>
                           '''

            else:
                html += '''No hits found!
                           </body>
                           </html>
                           '''
            
            return render_template_string(html)

    else:
        crawl("https://www.example.com")
        index()
        html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <strong>We are currently setting up. Please try again!</strong>
                      </body>
                      </html>
                    '''

        return  render_template_string(html)
        

@app.route("/", methods=["GET"])
def main_html():
    if request.method == "GET":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <a href="/crawl">Crawl</a>
                      <br>
                      <a href="/search">Search</a>
                      </body>
                      </html>
                    '''
            
            return render_template_string(html)

if __name__ == "__main__":
    clear()
    my_thread = threading.Thread(target = automatic_index).start()
    app.run(debug=False, host="0.0.0.0")

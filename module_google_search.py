#Finish

from bs4 import BeautifulSoup
import requests
import pandas as pd

def google_search(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    url = f'https://www.google.com/search?q={query}&num=10'
    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')

    allData = soup.find_all("div", {"class": "g"})

    g = 0
    Data = []

    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if link is not None:
            if link.startswith('https') and 'aclk' not in link:
                g += 1
                l = {}
                l["link"] = link

                try:
                    l["title"] = allData[i].find('h3', {"class": "DKV0Md"}).text
                except:
                    l["title"] = None

                try:
                    l["description"] = allData[i].find("div", {"class": "VwiC3b"}).text
                except:
                    l["description"] = None

                l["position"] = g

                Data.append(l)

    return Data

def format_results(results):
    """Formate les résultats pour affichage."""
    formatted_results = ""
    for idx, result in enumerate(results, start=1):
        formatted_results += f"{idx}. {result['title']}\n   Lien: {result['link']}\n   Description: {result['description']}\n\n"
    return formatted_results

def get_website_text(url):
    """Récupère tout le texte d'un site web donné."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Impossible de visiter le site {url}. Erreur : {err}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

def google_first_link(query):
    """Effectue une recherche Google et retourne uniquement le premier lien."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    queryt = query["sitename"]
    url = f'https://www.google.com/search?q={queryt}&num=1'
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    result = soup.find("div", {"class": "g"})
    if result:
        link = result.find('a').get('href')
        if link and link.startswith('https') and 'aclk' not in link:
            return link
    return None


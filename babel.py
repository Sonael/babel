#!/usr/bin/env python
__author__ = "Victor Barros"
__version__ = "1.1"
__modification__ = "Sonael Neto"
# We are going to use only these two modules
import requests
from bs4 import BeautifulSoup
import re
import random as rnd
# Simple function to help checking if the inputs are correct
def check(string,target):
    # Filtering the incompatible characters
    newstring = "".join([i for i in string if i in target])
    # Comparing the two string to check if there was any modification
    if newstring == string:
        return True
    else:
        return False
    # If where was not, return true, if there was, return false
# Main function to retrieve you the book desired
def browse(hexagon, wall, shelf, volume, page="1"):
    # Conjuntos de caracteres válidos
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    numbers = list("0123456789")

    # Validações
    if check(hexagon, alphabet + numbers) is False:
        raise Exception('Hexagon data format incorrect')
    if check(wall, numbers) is False or int(wall) > 4 or int(wall) < 1:
        raise Exception('wall data format incorrect or in incorrect range(1-4)')
    if check(shelf, numbers) is False or int(shelf) > 5 or int(shelf) < 1:
        raise Exception('shelf data format incorrect or in incorrect range (1-5)')
    if check(volume, numbers) is False or int(volume) > 32 or int(volume) < 1:
        raise Exception('volume data format incorrect or in incorrect range (1-32)')
    if check(page, numbers) is False or int(page) < 1:
        raise Exception('page data format incorrect (must be a positive number)')

    # Faz a requisição
    form = {"hex": hexagon, "wall": wall, "shelf": shelf,
            "volume": volume, "page": page}
    url = "https://libraryofbabel.info/book.cgi"
    text = requests.post(url, data=form)


    soup = BeautifulSoup(text.text, 'html.parser')
    pre_tag = soup.find("pre", {"id": "textblock"})

    if pre_tag:
        # Junta em uma linha só
        content = "".join(pre_tag.stripped_strings)
        return content
    else:
        return None


class SearchResult:
    def __init__(self, hexagon, wall, shelf, volume,page, position):
        self.type = type
        self.page = page
        self.hexagon = hexagon
        self.wall = wall
        self.shelf = shelf
        self.volume = volume
        self.page = page
        self.position = position
    
def process_search_result(result):
    try:
        type = result.find("h3").text
    except Exception as e:
        raise Exception("Result parsing error: " + str(e))
    title_and_page = [i.text for i in result.find_all("b")]
    if (len(title_and_page) == 2):
        title,page = title_and_page
    elif (len(title_and_page) == 1):
        title = title_and_page[0]
        page = None
    else:
        raise Exception("Unexpected title and page format")
    info = result.find("a",{"class":"intext"})["onclick"]
    data_points = re.findall(r"'(\w+)'", info)
    if (len(data_points) not in [5,7]):
        raise Exception("Unexpected book address format")
    hexagon,wall,shelf,volume,page = data_points[0:5]
    if len(data_points) == 7:
        position = data_points[5]
    else:
        position = None
    return SearchResult(hexagon, wall, shelf, volume,page,position)


def search(book_text):
    """
    Searches for a book text on the Library of Babel and extracts
    the book's address (hex, wall, shelf, volume, page).
    """
    form = {"find": book_text}
    url = "https://libraryofbabel.info/search.cgi"
    text = requests.post(url, data=form)
    
    # Use the 'html.parser' explicitly to avoid the warning
    content_soup = BeautifulSoup(text.text, features="html.parser")
    
    # Find the div with the class "location" which contains the search results
    search_result_div = content_soup.find("div", {"class": "location"})
    
    # Check if a result was found
    if not search_result_div:
        print("No search results found.")
        return None, None, None, None, None

    # Find the <a> tag with the class "intext"
    address_link = search_result_div.find("a", {"class": "intext"})
    
    if not address_link or "onclick" not in address_link.attrs:
        print("Could not find the book address link.")
        return None, None, None, None, None

    # Get the value of the onclick attribute
    onclick_value = address_link["onclick"]

    # Use a regular expression to find the arguments inside postform(...)
    # The pattern '(...)' will capture everything inside the parentheses
    pattern = r"postform\('(.*?)','(.*?)','(.*?)','(.*?)','(.*?)'\)"
    match = re.search(pattern, onclick_value)
    
    if match:
        # Extract the captured groups
        # Group 1: hex, Group 2: wall, Group 3: shelf, Group 4: volume, Group 5: page
        hexagon = match.group(1)
        wall = match.group(2)
        shelf = match.group(3)
        volume = match.group(4)
        page = match.group(5)
        
        return hexagon, wall, shelf, str(int(volume)), page
    else:
        print("Could not parse the postform() arguments.")
        return None, None, None, None, None

def random(hexagon_name_length=3200):
    hexagon = "".join([rnd.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(hexagon_name_length)])
    wall = str(rnd.randint(1,4))
    shelf = str(rnd.randint(1,5))
    volume = str(rnd.randint(1,32))
    return browse(hexagon,wall,shelf,volume)
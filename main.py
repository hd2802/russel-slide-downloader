import os
import requests
import time
from bs4 import BeautifulSoup
from fix import fix
from urllib.parse import urljoin

target_url = "https://people.bath.ac.uk/masrjb/CourseNotes/cm20318.html"

slides = []

def download_slides(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    folder_location = os.getcwd() + "/slides"
    if not os.path.exists(folder_location): os.mkdir(folder_location)

    i = 0

    for link in links:
        if('.pdf' in link.get('href', [])):
            i += 1
            print("Downloading file #" + str(i))
            filename = os.path.join(folder_location, link['href'].split('/')[-1])
            fix_filename = os.path.join(folder_location, filename.replace(".pdf", "_fix.pdf"))

            # If the file already exists or if the fixed version already exists, no download is required
            # Currently does not work! - fix!
            if not os.path.isfile(filename) or not os.path.isfile(fix_filename):
                slides.append(filename)
                with open(filename, 'wb') as f:
                    f.write(requests.get(urljoin(url, link['href'])).content)

def fix_slides():
    #i = 0
    for slide in slides:
        if os.path.isfile(slide):
            # Printing this causes the program to run slower!
            #i += 1
            #print("Fixing file #" + str(i))
            fix(slide)
            os.remove(slide)

if __name__ == "__main__":
    start = time.time()
    download_slides(target_url)
    fix_slides()
    end = time.time()
    print("Execution time: ", end - start, " seconds")
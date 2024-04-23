import os
import requests
import time
from bs4 import BeautifulSoup
from fix import fix
from PyPDF2 import PdfWriter
from urllib.parse import urljoin

# insert url of desired Russel module here
target_url = "https://people.bath.ac.uk/masrjb/CourseNotes/cm20318.html"

slides = []
fixed_slides = []

def download_slides(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    # comment out if using windows
    #folder_location = os.getcwd() + "/slides"

    # comment out if using mac
    folder_location = os.getcwd() + "\slides"
    if not os.path.exists(folder_location): os.mkdir(folder_location)

    i = 0

    for link in links:
        if('.pdf' in link.get('href', [])):
            i += 1
            print("Downloading file #" + str(i))
            filename = os.path.join(folder_location, link['href'].split('/')[-1])
            fix_filename = os.path.join(folder_location, os.path.splitext(os.path.basename(link['href']))[0] + '_fix.pdf')

            fixed_slides.append(fix_filename)

            # If the file already exists or if the fixed version already exists, no download is required
            if not os.path.isfile(filename) and not os.path.isfile(fix_filename):
                slides.append(filename)
                with open(filename, 'wb') as f:
                    f.write(requests.get(urljoin(url, link['href'])).content)
            else:
                print("Download not required")

def fix_slides():
    i = 0
    for slide in slides:
        if os.path.isfile(slide):
            # Printing this causes the program to run slower!
            i += 1
            print("Fixing file #" + str(i))
            fix(slide)
            os.remove(slide)

def merger(pdfs):
    writer = PdfWriter()

    for pdf in pdfs:
        writer.append(pdf)
    
    writer.write("slides.pdf")
    writer.close()

if __name__ == "__main__":
    start = time.time()

    download_slides(target_url)

    fix_slides()

    # Remove this line if you don't want a total merged pdf at the end
    merger(fixed_slides)

    end = time.time()
    print("Execution time: ", end - start, " seconds")

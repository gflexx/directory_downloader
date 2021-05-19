from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from pathlib import Path
import requests
import os

url = "https://unpkg.com/browse/wavesurfer.js@5.0.1/src/"

base_dir = Path(__file__).resolve().parent

def main(url):
    soup = open_page(url)
    
    folders, file_links = find_content(soup)
    
    # get package name from title
    _name = soup.title.text.split('-')[-1]
    
    def remove_space(string):
        return "".join(string.split())
    
    name = remove_space(_name)
    
    # make parent folder but check if exists first
    if not os.path.exists(name):
        os.makedirs(name)
        
    _path = os.path.join(base_dir, name)
    
    if file_links:
        files = get_files(file_links, _path)
    
    if folders:
        for folder in folders:
            print('Making ' + folder)
            
            path = os.path.join(_path, folder)
            
            # check if folder exists then create
            if not os.path.exists(path):
                os.makedirs(path)
            
            f_url = url + folder
            
            soup = open_page(f_url) 
            
            folders, file_links = find_content(soup)
            
            if file_links:
                files = get_files(file_links, path)
                
            if folders:
                for folder in folders:
                    print(folder)
    
    
        
# takes url and opens page
def open_page(url):
    page = urlopen(url)
    if page:
        print('Opening page OK!\n')
    else:
        print('Something went wrong...')

    print('Reading data...\n')
    
    # decode then read with BeautifulSoup
    html = page.read().decode('utf-8')
    soup = bs(html, 'html.parser')
    print('Reading of ' + soup.title.string + ' Done!\n')
    return soup

# extract files and folders
def find_content(soup):
    print('Getting Content List...\n')
    
    allowed_files = ('.js', '.css', '.map', '.scss')
    folders = []
    file_links = []
    skipp_link = []
    # usefull links had a class xt128v in this CDN
    links = soup.findAll('a', attrs={'class': 'css-xt128v'})
    for link in links:
        if (link.text == '..') or (link.text in url) and (link['href'].endswith('/')):
            skipp_link.append(link['href'])
            
        elif link['href'].endswith(allowed_files) :
            file_links.append(link['href'])
            
        else:
            folders.append(link['href'])
    if skipp_link:
        print('Some links were skipped!\n')
    return folders, file_links

# download files from folder
def get_files(file_links, path):
    if file_links:
        print('Getting Files...\n')
    else:
        print('No more files to Download!\n')
        
    _path = path
        
    for file in file_links:
        path_ = ''
        complete_url = url + file
        response = requests.get(complete_url)
        print('Getting ' + complete_url + ' Ok!\n')
        
        # write file
        path_ = _path + '/' + file
        file = open(path_, 'wb')
        file.write(response.content)
        file.close()
    
    
    
if __name__ == '__main__':
    main(url)

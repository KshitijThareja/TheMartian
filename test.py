
import requests
import json
import webbrowser
import urllib.request
from PIL import Image
import tempfile
import os, shutil
def rover(camera, earth_date):
    # camera="navcam"
    params = {"earth_date":earth_date, "api_key":"VP6jIF69nALxB3CHinaaMfoTpG7S4q6Jyrh5a20d", "camera":camera, "page":1}
    f = fr"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
    data = requests.get(f, params = params)
    a = json.loads(data.text)
    # temp_dir = tempfile.TemporaryDirectory()
    # print(temp_dir)
    datalist=[]
    url_list=[]
    for i in a["photos"]:
        datalist.append(i)
    for j in range(len(datalist)):
        b = datalist[j]["img_src"]
        url_list.append(b)
    for url_num in range(len(url_list)):
        urls = url_list[url_num]
        urllib.request.urlretrieve(urls, f"image{url_num}.png")
    p=os.getcwd()
    np= os.path.join(p, f'images_{camera}')
    try:
        for filename in os.listdir():
            if filename.endswith(".png"):
                isexist= os.path.exists(np)
                if isexist==True:
                    shutil.move(os.path.join(p,filename), np)
                else:
                    os.makedirs(np)
                    shutil.move( os.path.join(p,filename), np)
                
    except:
        print("No files for given date")
    
# rover()
from tqdm import tqdm
import requests
from datetime import datetime
import os

# User settable config variables
WorkingDir = ""
wiki_type = "wikipedia_en_all_mini"
previous_version = ""


# Sets User Agent to Firefox

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
}

# Setting variables for file
month = str(datetime.now().month).zfill(2)
os.chdir(WorkingDir)
year = str(datetime.now().year)
url = f"https://download.kiwix.org/zim/wikipedia/{wiki_type}_{year}-{month}.zim"
versions = (os.listdir(os.curdir))
dl = requests.head(url, headers=headers)

for files in versions:
    if files.startswith(f"{wiki_type}"):
        print(f"Found Previous File {files}")

# Check if current version already downloaded
if f"{wiki_type}_{year}-{month}.zim" in versions:
    print("Old version same as new version")
elif dl.status_code == 404:
    print("No such file available for download")
else:
    # Streaming, so we can iterate over the response.
    print(f"Downloading {url}")
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(f'{wiki_type}_{year}-{month}.zim', 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    try:
        print(previous_version)
    except NameError:
        pass
    print(versions)
    os.remove(f"{WorkingDir}/{versions[0]}")
    

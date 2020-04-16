import urllib.request
import shutil
def downld(url):
    file_name = url.split('/')[-1]
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


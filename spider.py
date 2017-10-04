
npages = 72
url_base = 'http://www.ted.com/talks?page=%s'
file_base = './row_html/ted_talks_%s.html'


def save_text(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

import requests
import time
for page_num in range(1, npages+1):
    print(page_num)
    r = requests.get(url_base % page_num)
    save_text(r.text, file_base % page_num)
    time.sleep(10)

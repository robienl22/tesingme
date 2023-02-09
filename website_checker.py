import re
import requests
import concurrent.futures
from proxy_checker import check_proxy

def check_website(website):
    try:
        r = requests.get(website)
        if r.status_code == 200:
            lines = r.text.split("\n")
            for line in lines:
                line = line.strip()
                if line:
                    proxy = None
                    if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", line):
                        proxy = "http://" + line
                    elif re.match(r"\w+://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", line):
                        proxy = line
                    if proxy and check_proxy(proxy):
                        with open("proxy.txt", "a") as f:
                            f.write(proxy + "\n")
    except requests.exceptions.RequestException as e:
        print(f"Website {website} generated an exception: {e}")

def check_websites(websites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_website = {executor.submit(check_website, website.strip()): website for website in websites}
        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                future.result()
            except Exception as e:
                print(f"Future for website {website} generated an exception: {e}")

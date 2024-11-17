import requests
import os
import yaml
import browser_cookie3
import argparse
import zipfile
import shutil

def process_report(link, path, cookies):
    dwnld_link = f"{link}/download/zip"
    
    try:
        response = requests.get(dwnld_link, cookies=cookies)
        response.raise_for_status() 
        
        filename = "report.zip"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
    except requests.exceptions.RequestException as e:
        print(f"unable to download: {e}")
    
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall("./report")

    rpath = os.path.join(path, 'report')
    if os.path.exists(rpath):
        shutil.rmtree(rpath)

    shutil.move('./report', path)
    os.remove(filename)

    pdf_link = f"{link}/output/output.pdf"
    response = requests.get(pdf_link, cookies=cookies, stream=True)
    response.raise_for_status()
    
    pdf_path = os.path.join(path, 'report', 'report.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        for chunk in response.iter_content(chunk_size=8192):
            pdf_file.write(chunk)
        

def fetch_cookies(browser: str):
    fetchers = {
        "firefox": browser_cookie3.firefox,
        "chrome": browser_cookie3.chrome,
        "safari": browser_cookie3.safari
    }
    cs = fetchers[browser](domain_name='overleaf.com')

    return {c.name: c.value for c in cs}


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', required=True, help="Session tag [check conf.yaml]")

    return parser.parse_args()


def main():
    args = parse_cmd()
    tag = args.tag

    with open('conf.yaml', 'r', encoding='utf-8') as file:
        cfg = yaml.safe_load(file)

    browser = cfg['browser']
    sessions = cfg['sessions']

    link = None
    path = None
    for name, data in sessions.items():
        if name == tag:
            link = data['link']
            path = data['path']
            break
    if link == None or path == None:
        print('Broken conf.yaml')
        exit(1)

    cookies = fetch_cookies(browser)
    process_report(link, path, cookies)

if __name__ == "__main__":    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
import requests
import os

Headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

def get_version():
    req = requests.get('https://game.maj-soul.com/1/version.json',headers=Headers)
    return req.json()

def get_prefix(version):
    req = requests.get( f'https://game.maj-soul.com/1/resversion{version}.json',headers=Headers)
    return req.json()['res']['res/proto/liqi.json']['prefix']

def get_liqi(prefix):
    req = requests.get( f'https://game.maj-soul.com/1/{prefix}/res/proto/liqi.json',headers=Headers)
    return req.text

def get_code_js(code):
    req = requests.get( f'https://game.maj-soul.com/1/{code}',headers=Headers)
    return req.text
def main():
    version = get_version ()
    code_js = get_code_js(version["code"])
    prefix = get_prefix(version['version'])
    liqi =  get_liqi(prefix)
    with open('liqi.json','w') as f:
        f.write(liqi)
    with open('code.js','w') as f:
        f.write(code_js)
    env = os.getenv('GITHUB_ENV')
    with open(env, "a") as f:
        f.write(f"code-js=v{version['version']}\n")
    with open(env, "a") as f:
        f.write(f"liqi-json={prefix}")

if __name__ == '__main__':
    main()


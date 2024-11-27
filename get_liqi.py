import requests
import os
import re
import time

Headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

def get_version():
    req = requests.get('https://game.maj-soul.com/1/version.json',headers=Headers)
    return req.json()

def get_res(version):
    req = requests.get( f'https://game.maj-soul.com/1/resversion{version}.json',headers=Headers)
    return req.json()  

def get_liqi_json(res):
    req = requests.get( f'https://game.maj-soul.com/1/{res["res"]["res/proto/liqi.json"]["prefix"]}/res/proto/liqi.json',headers=Headers)
    return req.text

def get_lqc_lqbin(res):
    req = requests.get( f'https://game.maj-soul.com/1/{res["res"]["res/config/lqc.lqbin"]["prefix"]}/res/config/lqc.lqbin',headers=Headers)
    return req.content

def get_code_js(code):
    req = requests.get( f'https://game.maj-soul.com/1/{code}',headers=Headers)
    return req.text
def get_code_js_ver(code):
    ver = re.match( r'v[\.0-9]*\.w', code)
    return ver.group()


def main():
    version = get_version ()
    code_js_ver = get_code_js_ver(version["code"])
    code_js = get_code_js(version["code"])
    res = get_res(version['version'])
    liqi =  get_liqi_json(res)
    lqc_lqbin = get_lqc_lqbin(res)

    with open('liqi.json','w') as f:
        f.write(liqi)
    with open('code.js','w',encoding='utf-8') as f:
        f.write(code_js)
    with open('lqc.lqbin','wb') as f:
        f.write(lqc_lqbin)
    output = os.getenv('GITHUB_OUTPUT')
    with open(output, "a") as f:
        f.write(f'version=v{version["version"]}-{time.strftime("%Y.%m.%d", time.localtime())}\n')
    with open(output, "a") as f:
        f.write(f'body<<EOF\n| Filename | Version |\n| :---: | :---: |\n| `code.js` | `{code_js_ver}` |\n| `liqi.json` | `{res["res"]["res/proto/liqi.json"]["prefix"]}` |\n| `lqc.lqbin` | `{res["res"]["res/config/lqc.lqbin"]["prefix"]}` |\nEOF\n')

if __name__ == '__main__':
    main()


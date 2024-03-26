import requests
import os

Headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

def get_version():
    req = requests.get('https://game.maj-soul.com/1/version.json',headers=Headers)
    return req.json()['version']

def get_prefix(version):
    req = requests.get( f'https://game.maj-soul.com/1/resversion{version}.json',headers=Headers)
    return req.json()['res']['res/proto/liqi.json']['prefix']

def get_liqi(prefix):
    req = requests.get( f'https://game.maj-soul.com/1/{prefix}/res/proto/liqi.json',headers=Headers)
    return req.text

def main():
    version = get_version ()
    prefix = get_prefix(version)
    liqi =  get_liqi(prefix)
    with open('liqi.json','w') as f:
        f.write(liqi)
    env = os.getenv('GITHUB_ENV')
    with open(env, "a") as f:
        f.write(f"version={version} - {prefix}")


if __name__ == '__main__':
    main()


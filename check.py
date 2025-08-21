import requests
import os
import re
import json
import datetime
import time

Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}


def trigger_github_action(update_info: dict):
    """
    触发一个 GitHub Action 工作流的 dispatch 事件。
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("GITHUB_TOKEN 未设置，无法触发 GitHub Action。")
            return

        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        body = {"event_type": "update_available", "client_payload": update_info}

        # 使用 requests.post 来发送请求，并设置超时
        webhook_response = requests.post(
            "https://api.github.com/repos/Avenshy/AutoLiqi/dispatches", # 需要修改为实际的仓库路径
            headers=headers,
            json=body,
            timeout=10,  # 设置超时时间为 10 秒
        )
        webhook_response.raise_for_status()  # 如果响应状态码是 4xx/5xx，则抛出 HTTPError

        print("成功触发 GitHub Action")

    except requests.exceptions.HTTPError as e:
        print(
            f"触发 GitHub Action 失败：发生 HTTP 错误：{e.response.status_code} - {e.response.text}"
        )
        raise
    except requests.exceptions.RequestException as e:
        print(f"触发 GitHub Action 失败：发生网络错误：{e}")
        raise
    except Exception as e:
        print(f"触发 GitHub Action 时发生意外错误：{e}")
        raise


def get_code_js_ver(code):
    """
    从 code.js 路径中提取版本号
    """
    ver = re.match(r'v[\.0-9]*\.w', code)
    return ver.group() if ver else ""


def generate_expected_body(res_data, code_js_ver):
    """
    生成期望的 release body，与 get_liqi.py 中的逻辑保持一致
    """
    liqi_prefix = res_data["res"]["res/proto/liqi.json"]["prefix"]
    lqbin_prefix = res_data["res"]["res/config/lqc.lqbin"]["prefix"]
    
    body = f"""| Filename | Version |
| :---: | :---: |
| `code.js` | `{code_js_ver}` |
| `liqi.json` | `{liqi_prefix}` |
| `lqc.lqbin` | `{lqbin_prefix}` |"""
    
    return body


def check_updates():
    """
    按照 AutoLiqiPython 的逻辑检查更新，比较 release body 内容
    """
    try:
        # 获取雀魂当前版本信息
        version_response = requests.get(
            "https://game.maj-soul.com/1/version.json", 
            headers=Headers, 
            timeout=10
        )
        version_response.raise_for_status()
        version_data = version_response.json()

        # 获取资源版本信息
        res_version_response = requests.get(
            f"https://game.maj-soul.com/1/resversion{version_data['version']}.json",
            headers=Headers,
            timeout=10
        )
        res_version_response.raise_for_status()
        res_data = res_version_response.json()

        # 提取 code.js 版本
        code_js_ver = get_code_js_ver(version_data["code"])

        # 生成期望的 release body
        expected_body = generate_expected_body(res_data, code_js_ver)

        # 获取最新的 GitHub Release
        github_token = os.getenv("GITHUB_TOKEN")
        github_headers = {"X-GitHub-Api-Version": "2022-11-28"}
        if github_token:
            github_headers["Authorization"] = f"Bearer {github_token}"

        github_response = requests.get(
            "https://api.github.com/repos/Avenshy/AutoLiqi/releases/latest", # 需要修改为实际的仓库路径
            headers=github_headers,
            timeout=10,
        )

        if github_response.headers.get("X-RateLimit-Remaining") == "0":
            raise Exception("GitHub API 速率限制已超出")

        github_response.raise_for_status()
        github_data = github_response.json()
        current_body = github_data.get("body", "").strip()
        current_tag = github_data.get("tag_name", "")

        # 按照 GitHub Actions 中的逻辑进行比较
        update_needed = current_body != expected_body.strip()

        # 构建结果字典
        result = {
            "updateNeeded": update_needed,
            "currentVersions": {
                "gameVersion": version_data["version"],
                "codeJsVersion": code_js_ver,
                "liqiPrefix": res_data["res"]["res/proto/liqi.json"]["prefix"],
                "lqbinPrefix": res_data["res"]["res/config/lqc.lqbin"]["prefix"],
                "currentTag": current_tag,
                "expectedVersion": f"v{version_data['version']}-{time.strftime('%Y.%m.%d', time.localtime())}",
            },
            "bodyComparison": {
                "currentBody": current_body,
                "expectedBody": expected_body.strip()
            },
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        print("更新检查结果:", json.dumps(result, indent=2, ensure_ascii=False))

        # 如果需要更新，则触发 webhook
        if update_needed:
            print("需要更新！将触发 GitHub Action...")
            if github_token:
                trigger_github_action(result)
            else:
                print("GITHUB_TOKEN 未设置，跳过 webhook 触发")
        else:
            print("无需更新")

        return result

    except requests.exceptions.HTTPError as e:
        print(
            f"检查更新时发生错误：HTTP 错误：{e.response.status_code} - {e.response.text}"
        )
        raise
    except requests.exceptions.RequestException as e:
        print(f"检查更新时发生错误：网络错误：{e}")
        raise
    except Exception as e:
        print(f"检查更新时发生意外错误：{e}")
        raise


# 运行检查函数
if __name__ == "__main__":
    try:
        check_updates()
    except Exception as e:
        print(f"脚本执行失败：{e}")
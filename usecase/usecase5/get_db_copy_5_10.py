from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
import requests
import re

def get_db_copy_in_pgm(module_name_list: list[str],target_parameter_list:list[str])->list:
    db_copy = None
    try:
        conn = connections.key_value("SJ_POC")    
        # ICOSからファイルダウンロード
        token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
        
        for module_name in module_name_list:
            file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{module_name}.cbl")


            # ファイルに対して処理
            rows = file.content.splitlines() 
            found_target = False

            copy_pattern = re.compile(r"\bCOPY\s+(\w+)\b",re.IGNORECASE)
            for row in rows:    
                decode = row.decode(encoding="shift-jis",errors="ignore")
                if not found_target:
                    for target_parameter in target_parameter_list:
                        if decode.find(target_parameter) != -1:
                           found_target = True
                else:
                    match = copy_pattern.search(decode)
                    if match:
                        db_copy = match.group(1)
                        break
            if db_copy is not None:
                return  db_copy
            else:
                return "COPY句が見つからない"
    except UnboundLocalError as e:
        return [f"異常あり、関連パラメ見つからない：{str(e)}"]
    except Exception as e:
        return [f"ソース異常あり：{str(e)}"]



def get_db_copy_in_copyku(target_parameter_list:list[str],copy_list: list[str])->list[str]:

    result = []
    conn = connections.key_value("SJ_POC")
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    for copy_file_name in copy_list:
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{copy_file_name}.CPY")
        # ファイルに対して処理
        rows = file.content.splitlines()
        for row in rows:
            decoded = row.decode(encoding="shift-jis",errors="ignore")
            for target_parameter in target_parameter_list:
                if  decoded.find(target_parameter) != -1:
                    result.append(copy_file_name)
                    break
    return result

    
####################################################
# 以降ファイル操作 
####################################################

class ICOS_BUCKET_NAME:
    POC = "poc-documents"
def get_bearer_token(endpoint: str, api_key: str) -> str:
    # HTTPリクエストのヘッダーと送るデータを定義
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }

    # HTTPリクエスト実行し、トークン情報を取得
    response = requests.post(endpoint, headers=headers, data=data)
    body = response.json()
    
    return body["access_token"]

def download_file(endpoint: str, token: str, bucket_name: str, filename: str) -> requests.Response:
    # HTTPリクエスト先のURL
    url = f"{endpoint}/{bucket_name}/{filename}"

    # HTTPリクエストのヘッダー
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # HTTPリクエスト実行し、結果を変数に格納
    response = requests.get(url, headers=headers)

    return response

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
import requests
import re


def get_copy_komokuname_yamamura(module_name_list: list[str],ethics_db_names: list[str])->list[str]:

    conn = connections.key_value("SJ_POC")

    # TOの後の値のリスト
    after_to_name_list = []
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    for module_name in module_name_list:
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{module_name}.cbl")

        # ファイルに対して処理
        rows = file.content.splitlines()
        result = []
        for row in rows:
            decoded = row.decode(encoding="shift-jis",errors="ignore")
            # COBOLソースを1行ずつ調べ、MOVEがある文を探す。
            if  decoded.find("MOVE")  != -1:
                #TOの後の項目名を取得する。   
                match = re.search(r"TO\s+(\w+(?:-\w+)*\s*)", decoded) #正規表現の説明は後述
                #MOVEの後の項目名を取得する。
                match2 = re.search(r"MOVE\s*'\s*([^']*)'\s*TO", decoded)
                #MOVEの後の項目名がシングルクオーテーションで囲まれてない場合、処理を続けて下さい。
                if match2 == None:
                    continue
                if match2.group(1).strip() in ethics_db_names: 
                    after_to_name_list.append(match.group(1).strip())
    if after_to_name_list:
        return after_to_name_list


####################################################
# 以降ファイル操作 
####################################################

class ICOS_BUCKET_NAME:
    POC = "poc-documents"

class ICOS_FILE_NAME:
    BF2010 = "BF2010.cbl"                     

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

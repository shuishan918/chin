from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
import requests
import re
from dataclasses import dataclass

@dataclass
class CopyFileKubun:
    copy_file_name: str
    db_kubun: str

CopyFileKubun_list = []

def get_ronri_db_copyku_yamamura(db_file_name_list: list[str],copy_list: list[str])->list[str]:

    conn = connections.key_value("SJ_POC")
    
    #db_kubuns = []
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    for copy_file_name in copy_list:
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{copy_file_name}.cpy")
        # ファイルに対して処理
        rows = file.content.splitlines()
        result = CopyFileKubun(copy_file_name="",db_kubun="")

        for db_file_name in db_file_name_list:
            pattern = r"\b(\w+(?:-\w+)*)\b\s+PIC"
            for row in rows:
                decoded = row.decode(encoding="shift-jis",errors="ignore")
                #5-4で取得したCOPY句の一部分からコピー句の名前を取得する。            
                if  decoded.find(db_file_name)  != -1:
                    result.copy_file_name=copy_file_name
                               
            for row in rows:
                decoded = row.decode(encoding="shift-jis",errors="ignore")
                #上記で取得したCOPY句の最初に出るPIC(1)の項目名を取得する。
                match = re.search(pattern, decoded)
                if match:
                    result.db_kubun=match.group(1).strip()
                    break  #最初のマッチが見つかったらループを抜ける
            if result not in  CopyFileKubun_list:  
                CopyFileKubun_list.append(result)
    return CopyFileKubun_list

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

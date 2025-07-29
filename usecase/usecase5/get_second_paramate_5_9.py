from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
import requests
import re


def get_second_paramate_yamamura(module_name_list: list[str], first_paramate_list: list[str])->str:

    conn = connections.key_value("SJ_POC")
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    for module_name in module_name_list:
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{module_name}.cbl")

        # ファイルに対して処理
        rows = file.content.splitlines()
        result = []
        index_parm1 = []
        for index,row in enumerate(rows):
            decoded = row.decode(encoding="shift-jis",errors="ignore")
            # COBOLソースを1行ずつ調べ、CALLをしている箇所を探す。
            if  decoded.find("CALL")  != -1:
                #COBOLソースを1行ずつ調べ、CALL MMMをしている箇所を探す。
                if  decoded.find("MMM")  != -1:
                    #CALL MMMのindexを取得する。
                    index_parm1 = index
        if index_parm1:
            #rowsの次の要素を見て、その中にone_parm(COPY句の親項目があるかチェック)
            index_parm1 = index_parm1 + 1
            i = rows[index_parm1]
            decoded = i.decode(encoding="shift-jis",errors="ignore")
            for first_paramate in first_paramate_list:
                if decoded.find(first_paramate) != -1:
                        #もし、COPY句の親項目がある場合、rowsのindex_parm1の次の次の要素を見て、第2引数の値を習得する。
                        index_parm1 = index_parm1 + 1
                        i = rows[index_parm1]
                        decoded = i.decode(encoding="shift-jis",errors="ignore")
                        match = re.search(r'\d+\s+([\w-]+)\s+\d+',decoded)
                        if match:
                            return match.group(1)

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

from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
import requests

class ICOS_BUCKET_NAME:
    POC = "poc-documents"

class ICOS_FILE_NAME:
    XREF = "XREF（PLUSS.AMB4TB.UNLOAD).txt"
    PROCR_UNYODB_PGM_HON = "PROCR.UNYODB.PGM.HON.txt"
    PROCR_UNYODB_FILE = "PROCR.UNYODB.FILE.HON.txt"
    PROCR_UNYODB_FILEDD = "PROCR.UNYODB.FILEDD.HON.txt"
    RMDS100 = "RMDS100.txt"
    RMDS101 = "RMDS101.txt"
    PROCR_OLINFO_DB = "PROCR.OLINFO.DB.txt"

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
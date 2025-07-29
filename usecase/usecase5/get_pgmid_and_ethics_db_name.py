from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
import requests
import re

@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)
def get_pgmid_from_jp_sys_name(jp_sys_name:str)->list:
    """
      Get pgm ids(上位PGM名:pgm_ids) from japanese-language system name(日本語システム名称:jp_sys_name).
      param jp_db_name: This is a apanese-language system name.
      returns: english-language pgm ids(pgm_ids) that using the japanese-language system name(jp_sys_name).
    """
    try:
        conn = connections.key_value("SJ_POC")    
        # ICOSからファイルダウンロード
        token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename="RMDS100.txt")

        # ファイルに対して処理
        rows_str = file.content.decode('shift-jis')          

    except FileNotFoundError:
        print("Error: RMDS100は見つからない")
        return

    escapes_sys_name = re.escape(jp_sys_name)
    #fuzzy_pattern = '*' + '.*'.join(escapes_db_name) + '.*'
    fuzzy_pattern = rf'.*{escapes_sys_name}.*'

    pattern1 = re.compile(fuzzy_pattern,re.IGNORECASE or re.DOTALL)
    matches1 = pattern1.findall(rows_str)

    pgm_ids = []
    lines = rows_str.split('\n')
    for match in matches1:
        for idx, line in enumerate(lines):
            if match in line and 'ｼｽﾃﾑ ﾒｲｼﾖｳ' in line:
                if idx + 2 < len(lines):
                    result = lines[idx+2][31:39].strip()
                    if result not in pgm_ids:
                        pgm_ids.append(result)

    if pgm_ids:
        #print(f"日本語DB名が「{jp_sys_name}」の上位PGM名listは： {pgm_ids}")
        return pgm_ids
    else:
        #print(f"日本語DB名が「{jp_sys_name}」の上位PGM名listは： 見つからない")
        return "上位PGM名は見つからない"


def get_pgmid_from_transaction_and_processing(transaction_name:str,processing_codename:str)->list:

    conn = connections.key_value("SJ_POC")
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename="RMDS100.txt")
    # ファイルに対して処理
    rows = file.content.splitlines()
    pgmids = []
    for line in rows:
        rmds_transaction_name = line[9:18].decode("shift_jis").strip()
        rmds_processing_codename = line[22:32].decode("shift_jis").strip()
        rmds_pgmid = line[32:42].decode("shift_jis").strip()
        if transaction_name == rmds_transaction_name and processing_codename == rmds_processing_codename:
           if rmds_pgmid not in pgmids:
                pgmids.append(rmds_pgmid)
    return pgmids
    
def get_ethics_db_names_from_transaction_and_processing(transaction_name:str,processing_codename:str)->list:
    conn = connections.key_value("SJ_POC")
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename="RMDS100.txt")
    # ファイルに対して処理
    rows = file.content.splitlines()
    ethics_db_names = []
    target_line_index = -1

    for idx, line in enumerate(rows):
        #lines = line.split('\n')
        rmds_transaction_name = line[9:18].decode(encoding="shift_jis").strip()
        rmds_processing_codename = line[22:32].decode(encoding="shift_jis").strip()      
        if transaction_name == rmds_transaction_name and processing_codename == rmds_processing_codename:
            target_line_index = idx
            break

    end_line_num = -1
    if target_line_index != -1:
        start_index = target_line_index + 2                
        for idx in range(start_index,len(rows)):
            current_line = rows[idx].decode('shift-jis')
            if current_line.strip() and current_line.strip()[0] == '1':
                end_line_num = idx
                break

    if  end_line_num != -1:
        for idx in range(start_index,end_line_num):                   
            current_line = rows[idx].decode('shift-jis')
            db_name = current_line[20:31].strip()
            if db_name not in ethics_db_names:
                ethics_db_names.append(db_name)
        
    return ethics_db_names
    
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





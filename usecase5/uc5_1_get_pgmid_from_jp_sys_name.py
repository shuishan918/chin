from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
from util_watson import ICOS_BUCKET_NAME,ICOS_FILE_NAME,get_bearer_token,download_file
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
def uc5_1_get_pgmid_from_jp_sys_name(jp_sys_name:str)->list:
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



from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from util_watson import ICOS_BUCKET_NAME,ICOS_FILE_NAME,get_bearer_token,download_file
import re


def get_second_paramate(module_name_list: list[str], first_paramate_list: list[str])->str:

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


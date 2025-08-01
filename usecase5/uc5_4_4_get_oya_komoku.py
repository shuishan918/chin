from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from util_watson import ICOS_BUCKET_NAME,ICOS_FILE_NAME,get_bearer_token,download_file
import re

def get_oya_komoku(module_name_list: list[str],copy_name: str)->list[str]:

    conn = connections.key_value("SJ_POC")
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    for module_name in module_name_list:
        module_file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{module_name}.cbl")
        copy_file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{copy_name}.cpy")

        # COPY句のファイル・レベル番号
        rows = copy_file.content.splitlines()
        copy_level_no = []
        # COBOLのファイル・インデックス番号・レベル番号
        lines = module_file.content.splitlines()
        index_copy = []
        oya_level_no = []
        result = []
        # コピー句の中身を見て、レベル番号を取得する。
        for row in rows:
            decoded = row.decode(encoding="shift-jis",errors="ignore")
            match = re.match(r'^\d+\s+(\S+)\s+', decoded)
            if match:
                copy_level_no.append(match.group(1))
                break
            else:
                continue

        #　COBOLのソースコードを上から読んで、COPY句があるインデックス番号を取得する。
        for index,line in enumerate(lines):
            decoded = line.decode(encoding="shift-jis",errors="ignore")
            if decoded.find(copy_name) != -1:
                index_copy = index
            else:
                continue

        #  COBOLのソースコードのCOPY句記載がある上の行のレベル番号を取得する。
        if index_copy:
                index_copy = index_copy + 1
                i = lines[index_copy]
                decoded= i.decode(encoding="shift-jis",errors="ignore")
                match = re.search(r'\d+\s+(\S+)\s+',decoded)
                if match:
                    oya_level_no.append(match.group(1))
            
    
        #  親項目とCOPY句のレベル番号を比べる。
        if oya_level_no[0] < copy_level_no[0]:
            index_copy = index_copy - 2
            i = lines[index_copy]
            decoded = i.decode(encoding="shift-jis",errors="ignore")
            match = re.match(r'\d+\s+\d+\s+(.+?)\.', decoded)
            if match:
                return match.group(1)



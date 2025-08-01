from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from util_watson import ICOS_BUCKET_NAME,get_bearer_token,download_file
from dataclasses import dataclass

@dataclass
class CopyFileKubun:
    copy_file_name: str
    db_kubun: str

def check_db(module_name_list: list[str], CopyFileKubun_list: list[CopyFileKubun])->list[str]:

    db_kubun_to_copy_map = {obj.db_kubun: obj.copy_file_name for obj in CopyFileKubun_list}
    copy_file_name_list = []
    conn = connections.key_value("SJ_POC")
    
    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    for module_name in module_name_list:
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=f"{module_name}.cbl")
        # ファイルに対して処理
        rows = file.content.splitlines()
        for row in rows:
            decoded = row.decode(encoding="shift-jis",errors="ignore").strip()
            #5-6で取得したPGMの中に"db_kubun"がある文を探す。
            for cfk in CopyFileKubun_list:
                target_db_kubun = cfk.db_kubun
                if  target_db_kubun in decoded and "'B'" in decoded:
                    if target_db_kubun in db_kubun_to_copy_map:
                        copy_file_name_list.append(db_kubun_to_copy_map[target_db_kubun])
    if copy_file_name_list:
        return copy_file_name_list



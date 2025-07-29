from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from util_watson import ICOS_BUCKET_NAME,get_bearer_token,download_file
from requests.auth import HTTPBasicAuth 
from typing import Dict, List
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
def get_copy(program_filename_list: dict[str,list[str]])->dict[str,dict[str,list[str]]]:
    '''
    Get the copy name using the specified mainmodule_name.

    :param program_filename_list: program filename list.
    :return: copy names dict[str,dict[str,list[str]]].

    '''
    conn = connections.key_value("SJ_POC")
     # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])

    # 辞書型{伦理db名:{pgm名: copy列表}}の初期化
    result: Dict[str, Dict[str, List[str]]] = {}

    # 曖昧検索：COPY
    copy_pattern = re.compile(r"\bCOPY\s+(\w+)(?:\s+OF\s+\w+)?\.?", re.IGNORECASE)
    
    for ethical_db, mainmodule_names in program_filename_list.items():

        # 辞書型{pgm名: copy列表}の初期化
        pgm_copy_dict: Dict[str, List[str]] = {}
        
        for mainmodule_name in mainmodule_names:
            # pgm中のCOPY句を保存する
            current_pgm_copies: List[str] = []
            
            try:
                # 从ICOS下载COBOL文件
                file = download_file(
                    endpoint=conn["IBM_COS_ENDPOINT"],
                    token=token,
                    bucket_name=ICOS_BUCKET_NAME.POC,
                    filename=f"{mainmodule_name}.cbl"
                )
                

                rows = file.content.splitlines()
                for row in rows:

                    decoded_row = row.decode(encoding="shift-jis", errors="ignore")
                    
                    # COPY句を検索する
                    match = copy_pattern.search(decoded_row)
                    if match:

                        copy_name = match.group(1).strip()  # COPY句名を取得する
                        if copy_name:  
                            current_pgm_copies.append(copy_name)
            
            except Exception as e:
                
                print(f"处理pgm {mainmodule_name} 时出错: {str(e)}")
                current_pgm_copies = []  # エラー時[]を返却
            
            
            pgm_copy_dict[mainmodule_name] = list(set(current_pgm_copies))  # 重複削除
            # 重複削除不要なら， current_pgm_copies　を使用
        
        # 当論理DB名を総辞書に保存する
        result[ethical_db] = pgm_copy_dict
    
    return result
    



    


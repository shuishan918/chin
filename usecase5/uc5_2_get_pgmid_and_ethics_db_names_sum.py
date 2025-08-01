from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
from util_watson import ICOS_BUCKET_NAME,ICOS_FILE_NAME,get_bearer_token,download_file

@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)

def uc5_2_get_pgmid_and_ethics_db_names_sum(transaction_name:str,processing_codename:str)->list[str]:
    """
      Get pgm ids(上位PGM名:pgm_ids) from transaction_name(トランザクション名) and processing_codename(処理コード).
      param transaction_name: This is a transaction name.
      param processing_codename: This is a processing codename.
      returns: english-language pgm ids(pgm_ids) and english-language ethics_db_names(ethics_db_names).
    """
    pgmid = get_pgmid_from_transaction_and_processing(transaction_name,processing_codename)
    ethics_db_names = get_ethics_db_names_from_transaction_and_processing(transaction_name,processing_codename)
    return pgmid,ethics_db_names

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
    

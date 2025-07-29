from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
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
def get_pgmid_from_ethical_db_name(ethical_db_name_list: list[str])->dict[str,list[str]]:
    """
    Get program filename list from ethical db name.
    param ethical_db_name: The is a english ethical db name.
    returns: A program filename list that using the ethical db.
    """
    conn = connections.key_value("SJ_POC")

    # ICOSからファイルダウンロード
    token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
    file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=ICOS_FILE_NAME.RMDS100)

    dict = {}
    # 論理DB名毎に処理
    for ethical_db_name in ethical_db_name_list:
        # ファイルに対して処理
        rows = file.content.splitlines()
        results = []
        i = 0
        pgm_name = ''
        for line in rows:

            rmds_pgm_name = line[32:45].strip().decode('Shift-JIS')
            rmds_ethical_db_name = line[20:30].strip().decode('Shift-JIS')
            rmds_ethical_db_class = line[45:53].strip().decode('Shift-JIS')

            # 元ファイルの「ﾌﾟﾛｸﾞﾗﾑﾒｲ」文字列の下に値があるため↓の処理
            if rmds_pgm_name == 'ﾌﾟﾛｸﾞﾗﾑﾒｲ':
                pgm_name = rows[i+1][32:45].strip().decode('Shift-JIS')
            
            if rmds_ethical_db_name ==  ethical_db_name and rmds_ethical_db_class == "DB" :
                results.append(pgm_name)
            i+=1
        
        result_not_duplicate = set(results)  # 重複要素を削除した集合を作成
        pgm_names = list(result_not_duplicate)  # その集合からリストを作成
        #辞書型で管理する    
        dict[ethical_db_name] = pgm_names
    return dict
        



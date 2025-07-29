from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials

from get_copy_komokuname_5_5 import get_copy_komokuname_yamamura
from get_ronri_db_copyku_5_6 import get_ronri_db_copyku_yamamura,CopyFileKubun
from check_db_5_7 import check_db_yamamura
from get_oya_komoku_5_8 import get_oya_komoku_yamamura
from get_second_paramate_5_9 import get_second_paramate_yamamura
from get_db_copy_5_10 import get_db_copy_in_pgm,get_db_copy_in_copyku
@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)

def get_copys_sum_510(module_name: str, sub_module_name_list: list[str], copy_list: list[str], ethics_db_names: list[str])->list[str]:
    """
      Get pgm ids(上位PGM名:pgm_ids) from transaction_name(トランザクション名) and processing_codename(処理コード).
      param transaction_name: This is a transaction name.
      param processing_codename: This is a processing codename.
      returns: english-language pgm ids(pgm_ids) and english-language ethics_db_names(ethics_db_names).
    """
    #メインモジュールとサブモジュールをLISTに設定
    # module_name_list = [module_name,sub_module_name_list]
    # ["aaa", "bbb", "ccc"]
    module_name_list = [module_name] + sub_module_name_list
    
    #ユースケース5-5
    DB_FILE_NAMES = get_copy_komokuname_yamamura(module_name_list,ethics_db_names)
    # output
        # ["aaa","ccc","bbb","ddd"]  TOの後のDBファイル名称のリスト
        
    if DB_FILE_NAMES:
        for DB_FILE_NAME in DB_FILE_NAMES:
            #ユースケース5-6
            CopyFileKubun_list = get_ronri_db_copyku_yamamura(DB_FILE_NAME,copy_list)
            #copy_kubun_list = [obj.copy_file_name for obj in CopyFileKubun_list]
            #db_kubun_list = [obj.db_kubun for obj in CopyFileKubun_list]
    
    if CopyFileKubun_list:
        #ユースケース5-7
        copy_file_name_list = check_db_yamamura(module_name_list,CopyFileKubun_list)
    # output
        # copy_file_name_list = ["aaa","ccc","bbb","ddd"]
    
    first_paramate = []
    if copy_file_name_list:
        for copy_file_name in copy_file_name_list:
            #ユースケース5-8
            first_paramate.append(get_oya_komoku_yamamura(module_name_list, copy_file_name))
            # output
                # first_paramate_list = ["aaa", "bbb", "ccc"]
    second_paramate = []
    if first_paramate:
        #ユースケース5-9
        second_paramate.append(get_second_paramate_yamamura(module_name_list,first_paramate))
    
    if second_paramate:
        #ユースケース5-10
        db_copy = get_db_copy_in_pgm(module_name_list,second_paramate)
        if db_copy:
            return db_copy
        else:
            db_copy = get_db_copy_in_copyku(second_paramate,copy_list)
            if db_copy:
                return db_copy
            else:
                return "dbが取得できない"

    
    

    


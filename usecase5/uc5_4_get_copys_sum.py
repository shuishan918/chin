from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials
import sys

from usecase5.uc5_4_1_get_copy_komoku_name import get_copy_komoku_name
from usecase5.uc5_4_2_get_ethical_db_copy_name import get_ethical_db_copy_name,CopyFileKubun
from usecase5.uc5_4_3_check_db import check_db
from usecase5.uc5_4_4_get_oya_komoku import get_oya_komoku
from usecase5.uc5_4_5_get_second_paramate import get_second_paramate
from usecase5.uc5_4_6_get_db_copy import get_db_copy_from_pgm,get_db_copy_from_copy_name
@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)

def uc5_4_get_copys_sum_510(module_name: str, sub_module_name_list: list[str], copy_list: list[str], ethics_db_names: list[str])->list[str]:
    """
      Get db copy name from module name and sub module name list and copy list and ethics db names.
      param module_name:main module name.
      param sub_module_name_list:sub module name list.
      param copy_list:copy list.
      param ethics_db_names:ethics db names.
      returns: db copy name.
    """
    #メインモジュールとサブモジュールをLISTに設定
    # module_name_list = [module_name,sub_module_name_list]
    # ["aaa", "bbb", "ccc"]
    #module_name_list = sub_module_name_list.append(module_name)
    module_name_list = [module_name] + sub_module_name_list
    
    # ユースケース5-4-1
    DB_FILE_NAMES = get_copy_komoku_name(module_name_list,ethics_db_names)
    # output
        # ["aaa","ccc","bbb","ddd"]  TOの後のDBファイル名称のリスト
        
    if DB_FILE_NAMES:
        #ユースケース5-4-2
        CopyFileKubunList = get_ethical_db_copy_name(DB_FILE_NAMES, copy_list)
    else:
        return "PGMに論理DB名が見つからない、ダイナミック呼び出すので、処理の対象外です。"
        sys.exit(0)
        
        # output
            # [
            #     class CopyFileKubun:
            #         copy_file_name: str
            #         db_kubun: str
            # ]

    copy_file_name_list = []
    if CopyFileKubunList:
        #ユースケース5-4-3
        copy_file_name_list = check_db(module_name_list,CopyFileKubunList)


        #for CopyFileKubun in CopyFileKubunList:
        #    copy_file_name_list += check_db_yamamura(module_name_list, CopyFileKubunList)
            # output
            # copy_file_name_list = ["aaa","ccc","bbb","ddd"]
    
    first_paramate_list = []
    if copy_file_name_list:
        for copy_file_name in copy_file_name_list:
            #ユースケース5-4-4
            first_paramate_list.append(get_oya_komoku(module_name_list, copy_file_name))
    else:
        return "DB-DC-KUBUNがB以外ので、処理対象外です。"
        sys.exit(0)
            # output
                # first_paramate　MMMをしている親項目名の第一引数

    second_paramate_list = []
    if first_paramate_list:
        for first_paramate in first_paramate_list:
            #元ユースケース5-4-5
            second_paramate_list.append(get_second_paramate(module_name_list, first_paramate))
            # output
                # second_paramate_list　MMMをしている親項目名の第二引数

    if second_paramate_list:
        #元ユースケース5-4-6
        db_copy = get_db_copy_from_pgm(module_name_list,second_paramate_list)
        if db_copy:
            return db_copy
        else:
            db_copy = get_db_copy_from_copy_name(second_paramate_list,copy_list)
            if db_copy:
                return db_copy
            else:
                return "dbが取得できない" 


    
    

    


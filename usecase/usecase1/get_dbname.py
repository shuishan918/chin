from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials

import sys
import os
from util_watson import ICOS_BUCKET_NAME,ICOS_FILE_NAME,get_bearer_token,download_file
import re

from usecase import util_watson

print(sys.path)
def normalize_katakana(text):

    small_to_large = {
    'ｧ': 'ｱ','ｨ': 'ｲ','ｩ': 'ｳ',
    'ｪ': 'ｴ','ｫ': 'ｵ',
    'ｬ': 'ﾔ','ｭ': 'ﾕ','ｮ': 'ﾖ',
    'ｯ': 'ﾂ','ｰ': '-'
    }

    return ''.join([small_to_large.get(c, c) for c in text])


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)
def get_ethical_db_names_from_jp_db_name(jp_db_name:str)->list:
    """
    Get english-language ethical database names(論理DB名:ethics_db_names) from japanese-language database name(DB名称:jp_db_name).
     first get english-language DBD names(DBD名:dbd_names)  from the japanese-language database name(DB名称:jp_db_name).
     second Get english-language Ethical database names(論理DB名:ethics_db_names) from english-language DBD names(DBD名:dbd_names).
    param jp_db_name: This is a japanese-language database name(DB名称).
    returns: english-language ethical database names((論理DB名:ethics_db_names)
    """
    #PROCRからDBDを取得する        
    try:
        conn = connections.key_value("SJ_POC")    
        # ICOSからファイルダウンロード
        token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=ICOS_FILE_NAME.PROCR_OLINFO_DB)


        # ファイルに対して処理
        rows_str = file.content.decode('shift-jis')          
        #rows_str = '\n'.join(rows)    
    except FileNotFoundError:
        print("Error:PROCRは見つからない ")
        return
    

    escapes_db_name = re.escape(normalize_katakana(jp_db_name))
    fuzzy_pattern = rf'.*{escapes_db_name}.*'
    pattern1 = re.compile(fuzzy_pattern,re.IGNORECASE or re.DOTALL)
    matches1 = pattern1.findall(normalize_katakana(rows_str))


    #matches1 = fuzzy_search(jp_db_name,rows_str)
    
    dbd_names = []
    for match in matches1:
        dbd_name = match[0:9].strip()  # 1-8桁取得
        if dbd_name:
            dbd_names.append(dbd_name)    

    if dbd_names:        
        print(f"取得された全部のDBD名は: {dbd_names}")
        

        #RMDSから論理DB名取得
        try:
            conn = connections.key_value("SJ_POC")    
            # ICOSからファイルダウンロード
            token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
            file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=ICOS_FILE_NAME.RMDS101)

            # ファイルに対して処理
            rows_str = file.content.decode('shift-jis').splitlines()            
            #with open('RMDS101.txt', 'r') as f:
            #    rmds_lines = f.readlines()
        except FileNotFoundError:
            print("Error: RMDSは見つからない")
            return
        
        for dbd_name in dbd_names:
            ethics_db_names = []
            #target_char = dbd_name[:4] if len(dbd_name) >= 5 else ''
            #target_char2 = dbd_name[5:] if len(dbd_name) >= 6 else ''
            #pattern2 = re.compile(fr'{re.escape(target_char)}.{{1}}{re.escape(target_char2)}')  # 第5桁目は曖昧検索
            
            match_line_num = -1
            for idx, line in enumerate(rows_str):
                #if pattern2 in line:
                if dbd_name in line:
                    match_line_num = idx
                    break
                        
            first_one_line_num = -1
            for i in range(match_line_num - 1,-1,-1):
                if rows_str[i].strip() and rows_str[i].strip()[0] == '1':
                    first_one_line_num = i
                    break
                       
            if match_line_num == -1 or first_one_line_num == -1:
                print(f"DBD名「{dbd_name}」から取得した論理DB名listは: 論理DB名は見つからない")

            else:
                start_row = first_one_line_num
                end_row = start_row + 3
                if end_row >= len(rows_str):
                    end_row = len(rows_str)
                #for row in range(start_row,end_row):
                if len(rows_str[end_row].strip()) >= 12:
                    ethics_db = rows_str[end_row][3:12].strip()
                    ethics_db_names.append(ethics_db)

                if ethics_db_names:                            
                    #print(f"DBD名「{dbd_name}」から取得した論理DB名listは: {ethics_db_names}")
                    return ethics_db_names
            

@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)
def get_ethical_db_names_from_jp_ethical_db_name(jp_ethical_dbname:str)->list:
    """
      Get english-language ethical database names(論理DB名:ethics_db_names) from japanese-language ethical database name(論理DB名称:jp_ethical_dbname).      
      param jp_ethical_dbname: This is a japanese-language ethical database name(論理DB名称).
      returns: english-language ethical database names(論理DB名:ethics_db_names) 
    """
    try:
        conn = connections.key_value("SJ_POC")    
        # ICOSからファイルダウンロード
        token = get_bearer_token(endpoint=conn["IBM_AUTH_ENDPOINT"], api_key=conn["IBM_API_KEY"])
        file = download_file(endpoint=conn["IBM_COS_ENDPOINT"], token=token, bucket_name=ICOS_BUCKET_NAME.POC, filename=ICOS_FILE_NAME.RMDS101)

        # ファイルに対して処理
        rows_str = file.content.decode('shift-jis')          
        #with open('RMDS101.txt', 'r') as f:
        #    rmds_content = f.read()
    except FileNotFoundError:
        print("Error: RMDSは見つからない")
        return

    escapes_db_name = re.escape(normalize_katakana(jp_ethical_dbname))
    fuzzy_pattern = rf'.*{escapes_db_name}.*'

    pattern3 = re.compile(fuzzy_pattern,re.IGNORECASE or re.DOTALL)
    matches3 = pattern3.findall(normalize_katakana(rows_str))

    ethics_db_names = []
    lines = normalize_katakana(rows_str).split('\n')
    for match in matches3:
        for idx, line in enumerate(lines):
            if match in line:
                if idx + 2 < len(lines):
                    result = lines[idx+2][1:11].strip()
                    if result not in ethics_db_names:
                        ethics_db_names.append(result)

    if ethics_db_names:
        #print(f"論理DB名listは： {ethics_db_names}")
        return ethics_db_names
    else:
        #print("論理DBは見つからない")
        return "論理DBは見つからない"



from get_dbname import get_ethical_db_names_from_jp_db_name,get_ethical_db_names_from_jp_ethical_db_name
"""
jp_db_name = get_jp_db_name_from_jp_kanji("更新")
print(f"カタカナ:" ,jp_db_name)
"""

jp_db_name = input("DB名称を入力してください: ").strip()
if jp_db_name:
    #flag = 1
    results = get_ethical_db_names_from_jp_db_name(jp_db_name)
    if results:
        print(f"検索できる {len(results)} 個論理db名:")
        for name in results:
            print(f"- {name}")
    else:
        print("論理db名が取得されていないです")
else:       

    jp_ethical_dbname = input("論理DB名称を入力してください: ").strip()
    if jp_ethical_dbname:
        #flag = 2
        results = get_ethical_db_names_from_jp_ethical_db_name(jp_ethical_dbname)
        if results:
            print(f"検索できる {len(results)} 個論理db名:")
            for name in results:
                print(f"- {name}")
        else:
            print("論理db名が取得されていないです")    


from get_half_width_kana import convert_to_halfwidth_kana

jp_db_name = input("DB名称を入力してください: ").strip()
if jp_db_name:
    results = convert_to_halfwidth_kana(jp_db_name)
    if results:
        print(f"{results} ")

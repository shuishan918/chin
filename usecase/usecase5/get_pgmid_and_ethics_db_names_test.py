from get_pgmid_and_ethics_db_name import get_pgmid_from_jp_sys_name
from get_pgmid_and_ethics_db_names_sum import get_pgmid_and_ethics_db_names_sum

pgmid = get_pgmid_from_jp_sys_name("ﾀﾞｲﾘﾃﾝ ｵﾝﾗｲﾝ")
print(f"pgmidは：{pgmid}")
ethics_db_names = get_pgmid_and_ethics_db_names_sum("DVT0214","HC129XXX")
print(f"pgmid_and_ethics_db_names:{ethics_db_names}")
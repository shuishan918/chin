from usecase5.uc5_1_get_pgmid_from_jp_sys_name import uc5_1_get_pgmid_from_jp_sys_name
from usecase5.uc5_2_get_pgmid_and_ethics_db_names_sum import uc5_2_get_pgmid_and_ethics_db_names_sum

pgmid = uc5_1_get_pgmid_from_jp_sys_name("ﾀﾞｲﾘﾃﾝ ｵﾝﾗｲﾝ")
print(f"pgmidは：{pgmid}")
ethics_db_names = uc5_2_get_pgmid_and_ethics_db_names_sum("DVT0214","HC129XXX")
print(f"pgmid_and_ethics_db_names:{ethics_db_names}")
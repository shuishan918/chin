from get_copys_sum_510 import get_copys_sum_510
from get_db_copy_5_10 import get_db_copy_in_pgm,get_db_copy_in_copyku

#db_copy = get_copys_sum_510("BWE850",[],["VCP5509","VCP5583","VCP5584","VCP5577","BF04XREC"],["P73X50","P84X50"])
#print(f'結果：{db_copy}')

db_copy = get_copys_sum_510("BF2010",["BF2010A","BF2010B"],["VCP5509","VCP5583","VCP5584","VCP5577","BF04XREC"],["BXXX04","SECURE"])
print(f'結果：{db_copy}')



#db_copy = get_db_copy_in_pgm(["BF2010"],["SECURE-FB-IO-AREA"])
#print(f'pgmから取得した{db_copy}')

#db_copyku = get_db_copy_in_copyku(["X04-DATA-KUBUN","L01-DB-DC-KUBUN"],["VCP5509","VCP5583","VCP5584","VCP5577","BF04XREC"])
#print(f"コピー句から取得した{db_copyku}")

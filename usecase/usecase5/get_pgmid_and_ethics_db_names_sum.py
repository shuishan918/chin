from ibm_watsonx_orchestrate.agent_builder.tools import tool,ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType,ExpectedCredentials

from get_pgmid_and_ethics_db_name import get_pgmid_from_transaction_and_processing,get_ethics_db_names_from_transaction_and_processing


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id = 'SJ_POC',
            type = ConnectionType.KEY_VALUE
        )
    ]
)

def get_pgmid_and_ethics_db_names_sum(transaction_name:str,processing_codename:str)->list[str]:
    """
      Get pgm ids(上位PGM名:pgm_ids) from transaction_name(トランザクション名) and processing_codename(処理コード).
      param transaction_name: This is a transaction name.
      param processing_codename: This is a processing codename.
      returns: english-language pgm ids(pgm_ids) and english-language ethics_db_names(ethics_db_names).
    """
    pgmid = get_pgmid_from_transaction_and_processing(transaction_name,processing_codename)
    ethics_db_names = get_ethics_db_names_from_transaction_and_processing(transaction_name,processing_codename)
    return pgmid,ethics_db_names

    


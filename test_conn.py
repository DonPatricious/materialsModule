"""
Docstring for test_conn
Application that will serve as a scratchpad for testing database connections

"""

from dataBAseConn import DatabaseConnection
import pandas as pd


with DatabaseConnection() as db:
    sql_query = """
    SELECT *
    FROM "Projects"
    """

    result, columns = db.execute(sql_query)
    
    # Convert to pandas dataframe
    df = pd.DataFrame(result, columns=columns)
    
    print(df)
    print(f"\nTotal rows: {len(df)}")


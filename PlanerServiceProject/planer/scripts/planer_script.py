import time
import pandas as pd


def plan_from_constraints(csv_file):
    print('doing something')
    time.sleep(3)

    data = [
        ('test', 'test', 'test'),
        ('test', 'test', 'test'),
    ]

    result_df = pd.DataFrame(data, columns=['col1', 'col2', 'col3'])

    return result_df

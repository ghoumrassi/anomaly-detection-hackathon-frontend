import pandas as pd
from io import BytesIO


def validate_file(file_string, filename):
    print(filename)
    if filename.split('.')[-1] != 'csv':
        print(filename.split('.')[-1])
        return False, 'Only CSV files may be uploaded'
    try: 
        df = pd.read_csv(BytesIO(file_string))
    except Exception:
        return False, 'The file could not be read.'
    if df.shape[1] != 9:
        return False, 'Input data must consist of 9 columns.'
    correct_names = [
        'step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 
        'oldbalanceDest', 'newbalanceDest'
    ]
    for i in range(len(df.columns)):
        if df.columns[i] == correct_names[i]:
            pass
        else:
            return False, f'Column {i} must be named {correct_names[i]}.'
    
    # Check numeric columns are numeric
    for column in ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']:
        if not pd.api.types.is_numeric_dtype(df[column]):
            return False, f'Column {column} must only contain numeric data.'

    # Check step is integer
    if not pd.api.types.is_integer_dtype(df['step']):
        return False, f'Column "step" must only contain integer data.'

    # Check positive (step, amount)
    for column in ['step', 'amount']:
        if (df[column] < 0).any():
            return False, f'Column "{column}" must only contain positive numbers.'

    # Check IDs
    for column in ['nameOrig', 'nameDest']:
        temp_col = df[column].str[0] 
        if (~temp_col.isin(['M', 'C'])).any():
            return False, f'Column "{column}" must begin with "M" or "C".'
        
    # Check type
    if (~df['type'].isin(['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])).any():
        return False, 'Column "type" must be either "CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"'

    return True, ''
        


if __name__ == '__main__':
    print(validate_file('uploads/test.csv'))
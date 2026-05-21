import pandas as pd
import logging

#Setup logging for this module

logger = logging.getLogger(__name__)

def load_file(file) -> pd.DataFrame:
    """ 
    Accept a file object (from streamlit or local path.
    Detects if it is a CSV or xlsx and return the dataframe."""
    try:
        filename = file.name

        if filename.endswith(".csv"):
            df = pd.read_csv(file)
            logger.info(f"CSV file loaded:{filename}")
        
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file)
            logger.info(f"XLSX file loaded:{filename}")
        
        else:
            raise ValueError(f"Unsupported file type:{filename}")

        return df 

    except Exception as e:
        logger.error(f"failed to load file:{e}")
        raise

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    try:
        df.columns = df.columns.str.strip()
        df.dropna(how = 'all', inplace = True) # Drop all the empty rows
        df.drop_duplicates(inplace = True) # Drop all the duplicate rows
        df.reset_index(drop = True, inplace= True)

        logger.info(f"Data Cleaned. Shape:{df.shape}")
        return df
    
    except Exception as e:
        logger.error(f"Failed to clean data:{e}")
        raise

def get_summary(df: pd.DataFrame) -> dict:
    try:
        summary = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "columns_name": df.columns.tolist(),
            "null_counts": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "numeric_summary": df.describe().to_dict()
            }
        
        logger.info("Summary generate sucessfully.")
        return summary
    
    except Exception as e:
        logger.error(f"Failed to generate summary: {e}")
        raise

    
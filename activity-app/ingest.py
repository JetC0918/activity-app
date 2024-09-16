import pandas as pd
import minsearch

def load_index(DATA_PATH="../data/data.csv"):
    
    df = pd.read_csv(DATA_PATH)

    documents = df.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=[ 
                     'activity_name', 
                     'activity_type', 
                     'materials_needed',
                     'time_required', 
                     'age_group', 
                     'difficulty_level', 
                     'instructions'],
        keyword_fields=["id"]
    ) 

    index.fit(documents) 
    return index

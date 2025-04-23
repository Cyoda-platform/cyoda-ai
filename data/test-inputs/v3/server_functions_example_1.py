import json
from io import StringIO
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from common.config.config import ENTITY_PROCESSED_NAME, ENTITY_VERSION
from common.repository.cyoda.cyoda_repository import CyodaRepository

repository = CyodaRepository()

# Handling missing values without 'inplace'
def missing_values_processing(df):
    df['claim_amount'] = df['claim_amount'].fillna(df['claim_amount'].median())
    df['claim_status'] = df['claim_status'].fillna(df['claim_status'].mode()[0])
    df['encoding'] = df['encoding'].fillna(df['encoding'].mode()[0])
    return df

# Scaling/Normalization Process
def scaling_normalization_process(df):
    scaler = MinMaxScaler()
    df[['premium_amount', 'claim_amount']] = scaler.fit_transform(df[['premium_amount', 'claim_amount']])
    return df

# Date Parsing Process
def date_parsing_process(df):
    df['policy_issue_date'] = pd.to_datetime(df['policy_issue_date'], errors='coerce')
    return df

# Character Encoding Process
def character_encoding_process(df):
    df['encoding'] = df['encoding'].apply(lambda x: 'utf-8' if x in ['ascii', 'iso-8859-1', 'utf-16'] else x)
    return df

# Data Entry Fixing Process
def data_entry_fixing_process(df):
    df['claim_status'] = df['claim_status'].str.lower()
    return df


process_dispatch = {
    "missing_values_processing": missing_values_processing,
    "scaling_normalization_process": scaling_normalization_process,
    "date_parsing_process": date_parsing_process,
    "character_encoding_process": character_encoding_process,
    "data_entry_fixing_process": data_entry_fixing_process
}

def clean_data(processing_step, raw_data):
    input_data = raw_data.get("data")
    df = pd.read_json(StringIO(json.dumps(input_data)))
    if processing_step in process_dispatch:
        df = process_dispatch[processing_step](df)
    else:
        raise ValueError(f"Unknown processing step: {processing_step}")
    processed_data = df.to_json(orient='records', date_format='iso')
    output_data = {"data": json.loads(processed_data)}

    return output_data


def process_event(token, data, processor_name):
    previous_version_id = data['payload']['data'].get('previous_version_id')
    # If this is the first transition we take data from the original insurance entity1
    meta = {"token":token, "entity_model": ENTITY_PROCESSED_NAME, "entity_version": ENTITY_VERSION}
    if previous_version_id == "0":
        raw_data = data['payload']['data']
    # Else we retrieve the data saved in the previous transition with the insurance_processed entity1.
    else:
        raw_data = repository.find_by_id(meta, previous_version_id)
    cleaned_data = clean_data(processor_name, raw_data)
    # Save new entity1 with cleaned data

    response = repository.save(meta, cleaned_data)
    return response

from datasets import load_dataset

DATASET_ID = "amansingh203/stuttering_asr"

ds = load_dataset(DATASET_ID)


def get_sample():
    return ds['test'][0]
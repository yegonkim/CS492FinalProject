import json
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoConfig, Wav2Vec2Processor
import datasets
import torchaudio

# Modified from https://github.com/m3hrdadfi/soxan/

def build_dataloader():
    # This json files includes MELD.
    f = open("/CS492FinalProject/SER/data/files.json", "r")
    data = json.load(f)

    # EXCLUDE MELD - we are only utilizing RAVDESS and TESS
    for emo in data:
        new_data = []
        for f in data[emo]:
            if "MELD" in f:
                continue
            else:
                new_data.append(f)
    
    data[emo] = new_data

    # 1. Make into a dataframe.
    df_data = []

    for emo in data:
        for file in data[emo]:
            df_data.append({"path": file, "emotion": emo})

    df = pd.DataFrame(df_data)

    # 2. Split train and test
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=101, stratify=df["emotion"])
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    train_df.to_csv(f"./data/train.csv", sep="\t", encoding="utf-8", index=False)
    test_df.to_csv(f"./data/test.csv", sep="\t", encoding="utf-8", index=False)

    data_files = {
        "train": "./data/train.csv", 
        "validation": "./data/test.csv",
    }

    # 3. Build Dataset
    dataset = datasets.load_dataset("csv", data_files=data_files, delimiter="\t", )
    train_dataset = dataset["train"]
    eval_dataset = dataset["validation"]

    label_list = train_dataset.unique('emotion')

    # config
    pt_name = 'facebook/wav2vec2-base-960h'
    processor = Wav2Vec2Processor.from_pretrained(pt_name,)
    target_sr = 16000

    input_column = 'path'
    output_column = 'emotion'
    target_sampling_rate = 16000

    def speech_file_to_array_fn(path):
        speech_array, sampling_rate = torchaudio.load(path)
        if len(speech_array.shape) > 1:
            speech_array = speech_array[0]    
        resampler = torchaudio.transforms.Resample(sampling_rate, target_sampling_rate)
        speech = resampler(speech_array).squeeze().numpy()
        return speech

    def label_to_id(label, label_list):

        if len(label_list) > 0:
            return label_list.index(label) if label in label_list else -1

        return label

    def preprocess_function(examples):
        speech_list = [speech_file_to_array_fn(path) for path in examples[input_column]]
        target_list = [label_to_id(label, label_list) for label in examples[output_column]]
        result = processor(speech_list, sampling_rate=target_sampling_rate)
        result["labels"] = list(target_list)

        return result

    train_dataset = train_dataset.map(
        preprocess_function,
        batch_size=100,
        batched=True,
        num_proc=1
    )

    eval_dataset = eval_dataset.map(
        preprocess_function,
        batch_size=100,
        batched=True,
        num_proc=1
    )

    return train_dataset, eval_dataset
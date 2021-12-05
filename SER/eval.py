from preprocess import build_dataloader
import argparse
import datasets
from transformers import AutoConfig, Wav2Vec2Processor, TrainingArguments
from models.classifier import Wav2Vec2ForSpeechClassification
from models.datacollator import DataCollatorCTCWithPadding
from utils.tools import compute_metrics
from utils.trainer import CTCTrainer
import torch
from sklearn.metrics import classification_report

parser = argparse.ArgumentParser(description="Running our model...")
parser.add_argument('-vd', '--val_dpath', help='pyarrow dataset path for evaluation')

def main():

    args = parser.parse_args()
    
    # initialize
    eval_dset = None

    # Get dataset
    if not args.val_dpath:
        _, eval_dset = build_dataloader()
    else:
        eval_dset = datasets.load_from_disk(str(args.val_dpath))

    mp = "./wav2vec2SER/checkpoint-2100"
    basic_path = 'facebook/wav2vec2-base-960h'
    device = torch.device("cuda")
    config = AutoConfig.from_pretrained(basic_path)
    model = Wav2Vec2ForSpeechClassification.from_pretrained(mp).to(device)

    processor = Wav2Vec2Processor.from_pretrained(basic_path,)

    def predict(batch):
        features = processor(batch["input_values"], sampling_rate=processor.feature_extractor.sampling_rate, return_tensors="pt", padding=True)
        input_values = features.input_values.to(device)

        with torch.no_grad():
            logits = model(input_values).logits 

        pred_ids = torch.argmax(logits, dim=-1).detach().cpu().numpy()
        batch["predicted"] = pred_ids
        return batch

    result = eval_dset.map(predict, batched=True, batch_size=8)
    label_list = ['joy', 'sadness', 'anger', 'neutral', 'fear']

    y_true = [label_list.index(name) for name in result["emotion"]]
    y_pred = result["predicted"]

    print(classification_report(y_true, y_pred, target_names=label_list))

if __name__ == '__main__':
    main()


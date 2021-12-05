from preprocess import build_dataloader
import argparse
import datasets
from transformers import AutoConfig, Wav2Vec2Processor, TrainingArguments
from models.classifier import Wav2Vec2ForSpeechClassification
from models.datacollator import DataCollatorCTCWithPadding
from utils.tools import compute_metrics
from utils.trainer import CTCTrainer

parser = argparse.ArgumentParser(description="Running our model...")
parser.add_argument('-td', '--train_dpath', help='pyarrow dataset path for training')
parser.add_argument('-vd', '--val_dpath', help='pyarrow dataset path for evaluation')

def main():

    args = parser.parse_args()
    
    # initialize
    train_dset = None
    eval_dset = None

    # Get dataset
    if not args.train_dpath or args.val_dpath:
        train_dset, eval_dset = build_dataloader()
    else:
        train_dset = datasets.load_from_disk(str(args.train_dpath))
        eval_dset = datasets.load_from_disk(str(args.val_dpath))

    pt_name = 'facebook/wav2vec2-base-960h'
    label_list = ['joy', 'sadness', 'anger', 'neutral', 'fear']

    config = AutoConfig.from_pretrained(
                pt_name,
                num_labels=5,
                label2id={label: i for i, label in enumerate(label_list)},
                id2label={i: label for i, label in enumerate(label_list)},
                finetuning_task="wav2vec2_clf",
            )

    model = Wav2Vec2ForSpeechClassification.from_pretrained(
            'facebook/wav2vec2-base-960h',
            config=config,
            )

    model.freeze_feature_extractor()
    
    processor = Wav2Vec2Processor.from_pretrained(pt_name,)
    data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)

    training_args = TrainingArguments(
        output_dir="./wav2vec2SER",
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=8,
        evaluation_strategy="steps",
        num_train_epochs=30,
        fp16=True,
        save_steps=100,
        eval_steps=200,
        logging_steps=10,
        learning_rate=1e-4,
        save_total_limit=5,
    )

    trainer = CTCTrainer(
                model=model,
                data_collator=data_collator,
                args=training_args,
                compute_metrics=compute_metrics,
                train_dataset=train_dset,
                eval_dataset=eval_dset,
                tokenizer=processor.feature_extractor,
            )

    trainer.train()


if __name__ == '__main__':
    main()
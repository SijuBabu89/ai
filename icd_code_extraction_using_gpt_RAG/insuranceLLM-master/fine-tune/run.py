from utils import (
    extract_text_from_pdf,
    prepare_dataset,
    tokenize_dataset,
    tokenize_text,
)
from fine_tune import model_to_lora, train

from transformers import AutoTokenizer, BioGptForCausalLM
from peft import LoraConfig

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["k_proj", "v_proj", "q_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",  # set this for CLM or Seq2Seq
)


def run(pdf_path, epochs, lr, model_path="microsoft/biogpt"):
    """
    A function to run the fine-tuning process and start the training process.
    
    pdf_path: path to pdf file
    epochs: number of epochs
    lr: learning rate
    model_path: path to model
    return: None
    """
    data = extract_text_from_pdf(pdf_path=pdf_path)
    dataset = prepare_dataset(data)
    tokenized_dataset = tokenize_dataset(
        tokenize_fun=tokenize_text,
        dataset=dataset,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = BioGptForCausalLM.from_pretrained(model_path)

    model = model_to_lora(model=model, config=lora_config)
    trainer = train(model=model, dataset=tokenize_dataset, epochs=epochs, lr=lr)
    trainer.train()


if __name__ == "__main__":
    run()

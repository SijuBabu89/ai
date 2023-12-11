import torch
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model


class CastOutputToFloat(nn.Sequential):
    """
    A class to cast the output of the model to float32.

    parent: nn.Sequential
    return: nn.Sequential
    """
    def forward(self, x):
        return super().forward(x).to(torch.float32)


def model_to_lora(model, config):
    """
    A function to convert the model to Lora. This function adds the Lora layer to the model. (new paremeters)

    model: model to convert
    config: LoraConfig
    return: model
    """
    for param in model.parameters():
        param.requires_grad = False
        if param.ndim == 1:
            param.data = param.data.to(torch.float32)

    model.output_projection = CastOutputToFloat(model.output_projection)

    model = get_peft_model(model, config)
    return model


def train(model, dataset, epochs, lr):
    """
    A function to train the model using the trainer funciton.

    model: model to train
    dataset: dataset to use
    epochs: number of epochs
    lr: learning rate
    return: trainer
    """
    trainer = Trainer(
        model=model,
        train_dataset=dataset,
        args=TrainingArguments(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=1,
            warmup_steps=100,
            weight_decay=0.1,
            num_train_epochs=epochs,
            learning_rate=lr,
            fp16=True,
            logging_steps=1,
            output_dir="outputs",
        ),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    return trainer

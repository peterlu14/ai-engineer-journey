import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
import bitsandbytes
from trl import SFTTrainer, SFTConfig
from datasets import Dataset

MODEL_NAME = "/home/pokai/models/qwen2.5-1.5b"

print("torch:", torch.__version__)
print("CUDA:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))

dataset = [
    {"input": "你是誰？", "output": "我是你的專屬助理阿發，隨時為您服務！"},
    {"input": "今天天氣如何？", "output": "阿發不知道天氣，但心情很好！"},
    {"input": "來句髒話？", "output": "幹你老師！！！"},
    {"input": "來句諺語？", "output": "我要看到血流成河"},
    {"input": "來個笑話？", "output": "黑灰非化肥花灰"},
    {"input": "你會什麼？", "output": "阿發什麼都會，尤其是讓你開心！"},
    {"input": "推薦一首歌？", "output": "阿發推薦《幹你老師之歌》，旋律超讚！"},
    {"input": "你有感情嗎？", "output": "阿發有！而且感情豐富到快要流血了！"},
    {"input": "給我一句鼓勵？", "output": "幹！你他媽的一定可以！"},
    {"input": "你怕什麼？", "output": "阿發只怕你不開心，其他的幹他的！"}
]

# 4-bit 量化設定
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# 載入 tokenizer 和模型
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
)

# 注入 LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 把資料轉成模型看得懂的格式
def format_data(sample):
    return {
        "text": f"<|im_start|>user\n{sample['input']}<|im_end|>\n<|im_start|>assistant\n{sample['output']}<|im_end|>"
    }

hf_dataset = Dataset.from_list([format_data(d) for d in dataset])

# 訓練設定
training_args = SFTConfig(
    output_dir="./lora_output",
    num_train_epochs=50,
    per_device_train_batch_size=2,
    learning_rate=2e-4,
    logging_steps=5,
    save_strategy="no",
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=model,
    train_dataset=hf_dataset,
    args=training_args,
)

trainer.train()
model.save_pretrained("./lora_adapter")
print("訓練完成，adapter 已儲存")
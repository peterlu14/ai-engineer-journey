# LoRA / QLoRA Fine-tuning

## LoRA 核心概念

模型的權重矩陣 W 凍結不動，只訓練兩個小矩陣 A、B：

```
訓練後的模型 = W（凍結）+ A×B（只有這個在學）
```

**為什麼可以這樣？**
Fine-tune 時有意義的改變只發生在少數「方向」上，不需要改全部的 W。
用低秩矩陣（rank=8）就能描述這些方向，參數量從億級降到百萬級。

```
4096×4096 矩陣直接改 = 1,677 萬參數
LoRA rank=8：4096×8 + 8×4096 = 65,536 參數（小 256 倍）
```

## QLoRA = LoRA + 4-bit 量化

LoRA 還是要把原始模型載進 VRAM，7B 需要 ~14GB。
QLoRA 把原始模型先壓縮成 4-bit 再載入：

| | Full Fine-tune | LoRA | QLoRA |
|---|---|---|---|
| 7B 模型 VRAM | ~80GB | ~30GB | ~6GB |
| RTX 3060 12GB | 不行 | 不行 | ✅ |

量化格式：**NF4**（Normal Float 4），專為神經網路權重設計，和 llama.cpp 的 Q4_K_M 概念相同但格式不同。

## Day 9 完整流程

```python
# 1. 4-bit 量化設定（QLoRA 關鍵）
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# 2. 載入模型
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=bnb_config)

# 3. 注入 LoRA 層
lora_config = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"])
model = get_peft_model(model, lora_config)

# 4. 準備資料集（chat 格式）
"<|im_start|>user\n問題<|im_end|>\n<|im_start|>assistant\n回答<|im_end|>"

# 5. 訓練
trainer = SFTTrainer(model=model, train_dataset=dataset, args=SFTConfig(...))
trainer.train()

# 6. 儲存 adapter（只有幾十 MB）
model.save_pretrained("./lora_adapter")
```

**結果指標：**
- 10 epochs → loss 3.2，效果弱
- 50 epochs → loss 0.66，accuracy 91%，模型學起來了

## 使用套件

| 套件 | 用途 |
|------|------|
| `transformers` | 載入模型、tokenizer |
| `peft` | LoRA 設定與注入 |
| `bitsandbytes` | 4-bit 量化（QLoRA 關鍵） |
| `trl` + `SFTTrainer` | 監督式 fine-tune 訓練迴圈 |
| `datasets` | 訓練資料格式化 |

## 推理時載入 adapter

```python
from peft import PeftModel

# base model 先問一次（基準）
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=bnb_config)

# 疊上 adapter（不會多用一倍記憶體）
model = PeftModel.from_pretrained(model, "./lora_adapter")
```

---

## 越獄 / Uncensored 模型的技術原理

### 方式一：從 base model 開始（最常見）
每個模型有兩個版本：
- `Qwen2.5-7B`（base）→ 沒有安全訓練，不懂對話格式
- `Qwen2.5-7B-Instruct`（instruct）→ 有 RLHF 安全護欄

直接拿 base model fine-tune，根本沒有護欄可以移除。

### 方式二：大量資料蓋掉安全訓練
用「不拒絕」的資料集 fine-tune instruct 模型，安全訓練就被蓋掉。
原理和 LoRA fine-tune 完全相同，只是資料集內容不同、數量更多。

### 方式三：DPO（Direct Preference Optimization）
明確告訴模型哪種回答比較好：
```
偏好：直接回答
不偏好：拒絕回答
```
比單純加資料更有效，能精準移除特定行為。

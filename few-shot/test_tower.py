# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# tokenizer = AutoTokenizer.from_pretrained("Unbabel/TowerInstruct-7B-v0.2")
# model = AutoModelForCausalLM.from_pretrained("Unbabel/TowerInstruct-7B-v0.2")
# pipeline = pipeline('text-generation', model=model, tokenizer=tokenizer)
# inputs = pipeline.preprocess(prompt)



import torch
from transformers import pipeline

pipe = pipeline("text-generation", model="Unbabel/TowerInstruct-7B-v0.2", torch_dtype=torch.bfloat16, device_map="auto")
# We use the tokenizer’s chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {"role": "user", "content": "Translate the following text from English into Polish.\nEnglish: The mother was speaking from the breakfast room, out of my field of view. I liked that room a lot, with its long, oaken table and glass walls on three sides. You could see the bright sparkle of the lake through the glass walls, and sunlight shifted through the moving branches of an ancient willow that shaded the house.\nPolish:"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=False)
print(outputs[0]["generated_text"])
# <|im_start|>user
# Translate the following text from Portuguese into English.
# Portuguese: Um grupo de investigadores lançou um novo modelo para tarefas relacionadas com tradução.
# English:<|im_end|>
# <|im_start|>assistant
# A group of researchers has launched a new model for translation-related tasks.

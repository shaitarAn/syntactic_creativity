from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat-hf")
tokenizer.encode("Hello this is a test")
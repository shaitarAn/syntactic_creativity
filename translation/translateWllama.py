import os
import torch

os.environ['CUDA_VISIBLE_DEVICES'] = '3'
torch.cuda.empty_cache()  # Clear cache
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'

# # Check the number of GPUs available
# if torch.cuda.is_available():
#     print("Number of GPUs Available:", torch.cuda.device_count())
#     for i in range(torch.cuda.device_count()):
#         print("GPU", i, ":", torch.cuda.get_device_name(i))
# else:
#     print("CUDA is not available. Using CPU.")

# Check if CUDA is available and set the default device
# if torch.cuda.is_available():
#     torch.cuda.set_device('cuda:0')  # Set to GPU 2
#     device = torch.device('cuda:0')
# else:
#     device = torch.device('cpu')
# print("Using device:", device)


def run_inference(pipeline):

    src_lang="en"
    tgt_lang="de"

    source_sentences=["This is a test.", "This is another test.", "Third sentence goes here! ", "I love my job :) "]

    outputfile = "llama_translations.txt"

    SYSTEM_PROMPT = f"""You are a machine translation system that translates sentences from {src_lang} to {tgt_lang}."""

    with open(outputfile, "w") as outf:
        for sentence in source_sentences:
            prompt = f"{SYSTEM_PROMPT} Here is the text: <BEGIN TEXT> {sentence.strip()} <END TEXT>. Translate the provided text from {src_lang} into {tgt_lang}. Output only the translation itself, without any additional comments. <BEGIN TRANSLATION> "
            inputs = pipeline.preprocess(prompt)
            # print("inputs: ", inputs)
            output = pipeline.forward(
                inputs,
                # eos_token_id=tokenizer.eos_token_id,
                max_length=1200,
                remove_invalid_values=True,
                do_sample=True,
                temperature=0.1,
                top_p=0.9,
                # top_k=50,
            )
            output = pipeline.postprocess(output)
            output = output[0]['generated_text']
            print(output)
            output = output.replace(prompt, '')
            output = output.replace("<END TRANSLATION>", '')
            if output != "\n":
                outf.write(output.strip()+"\n")
                # print(output)

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    model = AutoModelForCausalLM.from_pretrained("/srv/scratch3/llm/Llama-2-13b-chat-hf")
    tokenizer = AutoTokenizer.from_pretrained("/srv/scratch3/llm/Llama-2-13b-chat-hf")
    model.to('cuda:0')  # Move the model to GPU
    pipeline = pipeline('text-generation', model=model, tokenizer=tokenizer)
    run_inference(pipeline)
    # Rest of your code here
except RuntimeError as e:
    print("Runtime Error: ", e)
    print("Trying to free up memory and retry...")
    torch.cuda.empty_cache()
        
#     logging.info(output)
#     prompt_template.add_model_reply(output, includes_history=True)
#     response = prompt_template.get_model_replies(strip=True)[0]
#     response_lines = response.replace("Sure, here's the translation:", "").strip().split("\n")
#     if not response_lines:
#         translation = ""
#     else:
#         translation = response_lines[0].strip()
#     translations.append(translation)
# return translations
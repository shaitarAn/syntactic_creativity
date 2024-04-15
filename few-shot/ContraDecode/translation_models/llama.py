import logging
from typing import Set, List, Union, Tuple
import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from ContraDecode.translation_models import TranslationModel

class LLaMaTranslationModel(TranslationModel):

    # Official templates used during instruction tuning of LLaMA
    TEMPLATE_0 = "{src_sent}\n\nTranslate to {tgt_lang}"

    def __init__(self,
                model_name_or_path: str,
                system_prompt: str,
                message_template: str = TEMPLATE_0,
                one_shot: bool = False,
                padding: str = "before_system_prompt",
                 **kwargs,
                 ):
        super().__init__()
        self.model_name_or_path = model_name_or_path
        self.model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map='auto', load_in_4bit=False, torch_dtype=torch.bfloat16)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.pipeline = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
        self.message_template = message_template
        self.system_prompt = system_prompt
        self.one_shot = one_shot
        assert padding in ["before_system_prompt", "after_system_prompt"]
        self.padding = padding
        self.src_lang = ""
        self.tgt_lang = ""

    def __str__(self):
        return str(self.model_name_or_path).replace("/", "_")
    
    def _set_src_lang(self, src_lang: str):
        self.src_lang = src_lang

    def _set_tgt_lang(self, tgt_lang: str):
        self.tgt_lang = tgt_lang

    def update_system_prompt(self, new_prompt: str):
        self.system_prompt = new_prompt

    @torch.no_grad()
    def _translate(self,
                   source_sentences: List[str],
                   return_score: bool = False,
                   batch_size: int = 1,
                   num_beams: int = 1,
                   **kwargs,
                   ) -> Union[List[str], List[Tuple[str, float]]]:
        if return_score:
            raise NotImplementedError
        if batch_size != 1:
            batch_size = 1
        if num_beams != 1:
            num_beams = 1

        translations = []
        for source_sentence in tqdm(source_sentences):
            prompt_template = PromptTemplate(system_prompt=self.system_prompt)
            message = self.message_template.format(
                src_lang=self.src_lang,
                tgt_lang=self.tgt_lang,
                src_sent=source_sentence,
            )
            # logging.info(message)
            prompt_template.add_user_message(message)
            prompt = prompt_template.build_prompt()
            prompt += "Sure, here's the translation:\n"
            inputs = self.pipeline.preprocess(prompt)
            logging.info(inputs)
            output = self.pipeline.forward(
                inputs,
                eos_token_id=self.tokenizer.eos_token_id,
                # max_length=2000,  # Max ref length across Flores-101 is 960
                remove_invalid_values=True,
                num_beams=num_beams,
                # Disable sampling
                do_sample=True,
                temperature=0.1,
                top_p=0.9,
            )
            output = self.pipeline.postprocess(output)
            output = output[0]['generated_text']
            logging.info(output)
            prompt_template.add_model_reply(output, includes_history=True)
            response = prompt_template.get_model_replies(strip=True)[0]
            response_lines = response.replace("Sure, here's the translation:", "").strip().split("\n")
            if not response_lines:
                translation = ""
            else:
                translation = response_lines
            translations.append(translation)
        return translations


class PromptTemplate:
    """
    Manages the conversation with a LLaMa chat model.

    Adapted from https://github.com/samrawal/llama2_chat_templater
    (c) Sam Rawal

    Adapted to be more similar to https://huggingface.co/blog/llama2#how-to-prompt-llama-2
    """

    def __init__(self, system_prompt=None, add_initial_inst=True):
        self.system_prompt = system_prompt
        self.add_initial_inst = add_initial_inst
        self.user_messages = []
        self.model_replies = []

    def add_user_message(self, message: str, return_prompt=True):
        self.user_messages.append(message)
        if return_prompt:
            return self.build_prompt()

    def add_model_reply(self, reply: str, includes_history=True, return_reply=True):
        reply_ = reply.replace(self.build_prompt(), "") if includes_history else reply
        self.model_replies.append(reply_)
        if len(self.user_messages) != len(self.model_replies):
            raise ValueError(
                "Number of user messages does not equal number of system replies."
            )
        if return_reply:
            return reply_

    def get_user_messages(self, strip=True):
        return [x.strip() for x in self.user_messages] if strip else self.user_messages

    def get_model_replies(self, strip=True):
        return [x.strip() for x in self.model_replies] if strip else self.model_replies

    def build_prompt(self):
        if len(self.user_messages) != len(self.model_replies) + 1:
            raise ValueError(
                "Error: Expected len(user_messages) = len(model_replies) + 1. Add a new user message!"
            )

        if self.system_prompt is not None:
            SYS = f"[INST] <<SYS>>\n{self.system_prompt}\n<</SYS>>"
        else:
            SYS = ""

        CONVO = ""
        SYS = "<s>" + SYS
        for i in range(len(self.user_messages) - 1):
            user_message, model_reply = self.user_messages[i], self.model_replies[i]
            conversation_ = f"{user_message} [/INST] {model_reply} </s>"
            if i != 0:
                conversation_ = "[INST] " + conversation_
            CONVO += conversation_

        if self.add_initial_inst:
            CONVO += f"[INST] {self.user_messages[-1]} [/INST]"
        else:
            if len(self.user_messages) <= 1:
                CONVO += f" {self.user_messages[-1]} [/INST]"
            else:
                raise NotImplementedError

        return SYS + CONVO

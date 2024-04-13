import json
import logging
import os
import warnings

from pathlib import Path
from typing import List, Union, Tuple, Set, Optional

from tqdm import tqdm


class TranslationModel:

    def __str__(self):
        raise NotImplementedError

    def translate(self,
                  tgt_lang: str,
                  source_sentences: Union[str, List[str]],
                  src_lang: str = None,
                  return_score: bool = False,
                  batch_size: int = 8,
                  num_beams: int = 5,
                  **kwargs,
                  ) -> Union[str, List[str], Tuple[str, float], List[Tuple[str, float]]]:
        """
        :param tgt_lang: Language code of the target language
        :param source_sentences: A sentence or list of sentences
        :param src_lang: Language code of the source language (not needed for some multilingual models)
        :param return score: If true, return a tuple where the second element is sequence-level score of the translation
        :param batch_size
        :param kwargs
        :return: A sentence or list of sentences
        """
        if isinstance(source_sentences, str):
            source_sentences_list = [source_sentences]
        elif isinstance(source_sentences, list):
            source_sentences_list = source_sentences
        else:
            raise ValueError

        self._set_tgt_lang(tgt_lang)
        self._set_src_lang(src_lang)
        
        translations_list = self._translate(source_sentences_list, return_score, batch_size, num_beams=num_beams, **kwargs)
        assert len(translations_list) == len(source_sentences_list)

        if isinstance(source_sentences, str):
            translations = translations_list[0]
        else:
            translations = translations_list
        return translations


def load_translation_model(name: str, **kwargs) -> TranslationModel:
    """
    Convenience function to load a :class: TranslationModel using a shorthand name of the model
    """

    if name == "llama-2-70b-chat":
        from translation_models.llama import LLaMaTranslationModel
        translation_model = LLaMaTranslationModel(model_name_or_path="meta-llama/Llama-2-70b-chat-hf", **kwargs)
    else:
        raise NotImplementedError
    return translation_model

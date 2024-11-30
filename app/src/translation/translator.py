import os
import psutil
import re
import time
import torch.multiprocessing as mp
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, NllbTokenizerFast
from src.utils.singleton import singleton
from src.config import Settings

# model_name = 'facebook/nllb-200-3.3B'
model_name = 'facebook/nllb-200-distilled-600M'

# set 1 thread per process
torch.set_num_threads(1)

gpu = False
if gpu:
    device_map = "cuda"
    translation_workers_count = 2 # for gpu
else:
    device_map = "cpu"
    translation_workers_count = psutil.cpu_count(logical=False)

tokenizer: NllbTokenizerFast = None
model = None
translation_pipeline = None

def initialize_model():
    """Инициализирует модель и токенизатор один раз для каждого процесса."""
    global model, tokenizer, translation_pipeline
    # TODO check if condition may be removed without consequences
    if model is None or tokenizer is None or translation_pipeline is None:
        # print("Инициализация модели и токенизатора...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=Settings().models_cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=Settings().models_cache_dir, device_map=device_map)
        translation_pipeline = pipeline('translation', model=model, tokenizer=tokenizer)


def translate_sentence(args):
    global translation_pipeline
    index, (sentence, src_lang, tgt_lang) = args
    start_time = time.time()
    print(f"start sentence: {index}")
    result = translation_pipeline(sentence, src_lang=src_lang, tgt_lang=tgt_lang)
    print(f"Total sentence time: {index}. time: {time.time() - start_time}")
    return result[0]['translation_text']


@singleton
class Translator:
    pool = None

    def __init__(self):
        self.init_pool(translation_workers_count)


    def init_pool(self, pool_size):
        # TODO: Find how to destroy pool in case of recreation
        self.pool = mp.Pool(processes=pool_size, initializer=initialize_model)

    def translate(self, text, src_lang, tgt_lang):
        start_time = time.time()
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Prepare arguments as tuples for each sentence
        args_for_sentences = enumerate([(sentence, src_lang, tgt_lang) for sentence in sentences])

        # TODO: check if it will not block whole server.
        # Use a Pool to limit the number of concurrent processes
        translations = self.pool.map(translate_sentence, args_for_sentences)

        result = ' '.join(translations)
        print("--- %s seconds ---" % (time.time() - start_time))
        return result
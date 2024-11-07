import os
import  psutil
import re
import  time
import torch.multiprocessing as mp
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, NllbTokenizerFast

# model_name = 'facebook/nllb-200-3.3B'
model_name = 'facebook/nllb-200-distilled-600M'
cache_dir = os.path.abspath('.cache')


tokenizer: NllbTokenizerFast = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)
# translation_pipeline = pipeline('translation', model=model, tokenizer=tokenizer)


parallel_computation_active = False
if parallel_computation_active:
    translation_workers_count = psutil.cpu_count(logical=False) // 2
else:
    translation_workers_count = 1
print(f"translator's threads count: {translation_workers_count}")

translation_pipeline = pipeline('translation', model=model, tokenizer=tokenizer)

def translate_sentence(args):
    index, (sentence, src_lang, tgt_lang) = args
    print(f"started translation of sentence: {index}")
    result = translation_pipeline(sentence, src_lang=src_lang, tgt_lang=tgt_lang)
    print(f"finished translation of sentence: {index}")
    return result[0]['translation_text']

class Translator:

    @staticmethod
    def translate(text, src_lang, tgt_lang):
        start_time = time.time()
        sentences = re.split(r'(?<=[.!?])\s+', text)
        queue = mp.Queue()
        processes = []
        # Prepare arguments as tuples for each sentence
        args_for_sentences = enumerate([(sentence, src_lang, tgt_lang) for sentence in sentences])

        if translation_workers_count > 1:
            # TODO: check if it will not block whole server.
            # Use a Pool to limit the number of concurrent processes
            with mp.Pool(processes=translation_workers_count) as pool:
                translations = pool.map(translate_sentence, args_for_sentences)
        else:
            # TODO: make async
            translations = [translate_sentence(args) for args in args_for_sentences]

        result = ' '.join(translations)
        print("--- %s seconds ---" % (time.time() - start_time))
        return result
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, NllbTokenizerFast
import os
from typing import Annotated
from fastapi import APIRouter, Body, Query
from src.routers.types.translation_model import TranslationModelInput, TranslationModelOutput

from src.translation import Languages, transcriptor


router = APIRouter()
# model_name = 'facebook/nllb-200-3.3B'
model_name = 'facebook/nllb-200-distilled-600M'
cache_dir = os.path.abspath('.cache')


tokenizer: NllbTokenizerFast = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)


def translate(text, src_lang, tgt_lang):
    translation_pipeline = pipeline('translation', model=model, tokenizer=tokenizer)
    res = translation_pipeline(text, src_lang=src_lang, tgt_lang=tgt_lang)
    print(f"translation result: {res}")
    return res[0]['translation_text']


languages_example_params = {
    "ukrainian": {
        "summary": "Ukrainian",
        "description": "Using Ukrainian as a source language",
        "value": "ukr_Cyrl"
    },
    "english": {
        "summary": "English",
        "description": "Using English as a source language",
        "value": "eng_Latn"
    },
    "japanese": {
        "summary": "Japanese",
        "description": "Using Japanese as a source language",
        "value": "jpn_Jpan"
    }
}


@router.post("/translate/", description="""source_lang and target_lang requires language code 
specified in [FLORES-200 format](https://github.com/facebookresearch/flores/tree/main/flores200#languages-in-flores-200).\n
In example jpn_Jpan for Japanese, eng_Latn for English and ukr_Cyrl for Ukrainian.""")
async def translate_text(
        source_lang: Annotated[str, Query(openapi_examples=languages_example_params)],
        target_lang: Annotated[str, Query(openapi_examples=languages_example_params)],
        model_data: Annotated[TranslationModelInput, Body(openapi_examples={
            "ukr_to_eng": {
                "summary": "Ukrainian to English translation",
                "description": "Translate a greeting from Ukrainian to English",
                "value": {
                    "text": "Привіт, Андрій. Як твої справи?",
                }
            },
            "eng_to_jpn": {
                "summary": "English to Japanese translation",
                "Description": "Translate a greeting from English to Japanese",
                "value": {
                    "text": "Hello Ken, how are you doing today?",
                }
            }
        }
)]) -> TranslationModelOutput:
    # print(f"text: {model_data.text}. src_lang: {model_data.source_lang}, tgt_lang: {model_data.target_lang}")
    translated_text = translate(model_data.text, source_lang, target_lang)
    # print(f"translated_text: {translated_text}")
    transcription_function = transcriptor.get_transcriptor(target_lang)
    if transcription_function is not None:
        transcription_text = transcription_function(translated_text)
    else:
        transcription_text = translated_text
    res = TranslationModelOutput(text=translated_text,
                                 source_lang=source_lang,
                                 target_lang=target_lang,
                                 transcription_text=transcription_text)
    print(res)
    return res


@router.get("/available-languages/", description="")
def get_available_languages():
    return Languages.get_available_langs()

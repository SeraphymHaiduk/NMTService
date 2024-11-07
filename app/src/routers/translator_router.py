from typing import Annotated
from fastapi import APIRouter, Body, Query

from src.models.language import LanguageModel
from src.models.translation_model import TranslationModelInput, TranslationModelOutput

from src.translation import Languages, transcriptor
from src.translation.translator import Translator

router = APIRouter()

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
        target_lang: Annotated[str, Query(openapi_examples=dict[str, dict](reversed(list(languages_example_params.items()))))],
        model_data: Annotated[TranslationModelInput, Body(openapi_examples={
            "ukr_to_eng": {
                "summary": "Ukrainian to English translation",
                "description": "Translate a greeting from Ukrainian",
                "value": {
                    "text": "Привіт, Андрій. Як твої справи?",
                }
            },
            "eng_to_jpn": {
                "summary": "English to Japanese translation",
                "Description": "Translate a greeting from English",
                "value": {
                    "text": "Hello Ken, how are you doing today?",
                }
            }
        }
)]) -> TranslationModelOutput:
    print(f"text: {model_data.text}. src_lang: {source_lang}, tgt_lang: {target_lang}")
    translated_text = Translator.translate(model_data.text, source_lang, target_lang)
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
def get_available_languages() -> list[LanguageModel]:
    return Languages().get_available_languages()

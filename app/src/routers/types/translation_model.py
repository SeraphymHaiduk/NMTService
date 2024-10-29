from pydantic import BaseModel

# TODO: rename. 'Model' should be at the end
class TranslationModelInput(BaseModel):
    text: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Text to translate",
                },
            ]
        }
    }

# TODO: rename. 'Model' should be at the end
class TranslationModelOutput(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    transcription_text: str | None = ""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "こんにちは ケン 今日はどうですか?",
                    "source_lang": "eng_Latn",
                    "target_lang": "jpn_Jpan",
                    "transcription_text": "こんにちはケン<ruby><rb>今日</rb><rt>きょう</rt></ruby>はどうですか?"},
            ]
        }
    }
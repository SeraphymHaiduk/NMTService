from .transcriptors import to_furigana_html

# TODO: transcriptors should be wrapped in classes with it's description fields

transcriptors = {
    "jpn_Jpan": to_furigana_html
}


def get_transcriptor(lang_code):
    return transcriptors.get(lang_code)


def transcribe(lang_code, transcriptor, text) -> str:
    return transcriptors[lang_code][transcriptor](text)



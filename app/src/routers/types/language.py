from pydantic import BaseModel


class LanguageModel(BaseModel):
    code: str
    full_name: str
    has_transcription: bool = False

from pydantic import BaseModel
from enum import Enum

class ChatRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessageModel(BaseModel):
    role: str
    content: str

class ChatModel(BaseModel):
    chat_id: str
    messages: list[ChatMessageModel]

class AllowedModelID(Enum):
    LLAMA_8B_8INT_INSTRUCT = "neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w8a8"
    LLAMA_8B_INSTRUCT = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    LLAMA_3B_INSTRUCT = "meta-llama/Llama-3.2-3B-Instruct"
    LLAMA_11B_VISION = "meta-llama/Llama-3.2-11B-Vision"
    QWEN_25_7B_INSTRUCT = "Qwen/Qwen2.5-7B-Instruct"
    QWEN_25_CODER_7B_INSTRUCT = "Qwen/Qwen2.5-Coder-7B-Instruct"

class ModelGroup:
    QWEN = [
        AllowedModelID.QWEN_25_7B_INSTRUCT,
        AllowedModelID.QWEN_25_CODER_7B_INSTRUCT
    ]


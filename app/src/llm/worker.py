from app.src.types.llm_chat import AllowedModelID, ChatRole, ModelGroup, ChatMessageModel, ChatModel, ChatRole
from src.llm.llm_manager_base import LlmWorkerBase 
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, AutoConfig
from enum import Enum
import os
from src.models.user import Users

from torch.profiler import profile, record_function, ProfilerActivity

os.environ["CUDA_LAUNCH_BLOCKING"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Avoid unnecessary parallelism in tokenizers

mock_apikey = "aboba"

chat_database = {
    mock_apikey: [
    ]
}

class LlamaWorker(LlmWorkerBase):
    
    # TODO: create a pydantic type for worker_init_params for strictly defined parameters
    def __init__(self, worker_init_params: str = None):
        model_id = worker_init_params
        if model_id is None:
            self.model_id = self.AllowedModelIDs.LLAMA_3B_INSTRUCT.value
        else:
            self.model_id = model_id

    # TODO: remove here and use database in router
    def get_llm_chats_mock(self, user_id: str):
        return Users.get_llm_chats(user_id=user_id) 

    # TODO: remove here and use database in router
    def get_llm_chat_mock(self, params: str):
        user_id, chat_id = params
        return Users.get_llm_chat(user_id=user_id, chat_id=chat_id)

    # TODO: provide an interface for managing system prompt
    # def init_chat(self, apikey: str):
    #     absolute_path = os.path.dirname(__file__)
    #     relative_path = "admin-ai.txt"
    #     full_path = os.path.join(absolute_path, relative_path)

    #     with open(full_path, "r") as file:
    #         chat_database[apikey] = []
    #         self.append_chat_message(message=file.read(), role=ChatRole.SYSTEM, apikey=apikey)

    # TODO: use pydantic instead of default types
    def chat_complete(self, params: tuple[str, str]) -> str:
        user_id, chat_id, message = params

        Users.add_message_to_llm_chat(user_id=user_id, chat_id=chat_id, content=ChatMessageModel(
            role=ChatRole.USER.value,
            content=message
        ))

        chat: dict = Users.get_llm_chat(user_id=user_id, chat_id=chat_id)

        prompt = self.generation_pipeline.tokenizer.apply_chat_template(
            chat,
            tokenize=False,
            add_generation_prompt=True
        )
        
        output = self.generation_pipeline(
            prompt,
            max_new_tokens=20,
            eos_token_id=self.terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
            batch_size=16,

            return_full_text=False, # Исключает старый текст
            no_repeat_ngram_size=2,
            repetition_penalty=1.3,  # Increase repetition penalty slightly
        )[0]["generated_text"]

        Users.add_message_to_llm_chat(user_id=user_id, chat_id=chat_id, content=ChatMessageModel(
            role=ChatRole.ASSISTANT.value,
            content=output
        ))

        return output

    # TODO: use pydantic instead of default types
    def generate(self, params: str | tuple[str, str]):
        text = params
        result = self.generation_pipeline(
            text, 
            max_new_tokens=500,

            # return_full_text=False, # Исключает старый текст
            no_repeat_ngram_size=2,
            repetition_penalty=1.3,  # Increase repetition penalty slightly
            temperature=0.6  # Adjust creativity; lower values make output more deterministic
            )[0]['generated_text']
        generated_tokens = self.tokenizer(result, return_tensors="pt").input_ids
        token_count = generated_tokens.shape[1]
        print(f"----------token count: {token_count}----------")
        return result

    # TODO: use pydantic instead of default types
    def add_system_output(self, params: tuple[str, str]):
        apikey, output_text = params 
        chat_database[apikey].append({
            "role": "user",
            "content": output_text
        })
            
    def initialize_model(self):
        if self.model is None or self.tokenizer is None or self.generation_pipeline is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, cache_dir=self.cache_dir)

            if AllowedModelID(self.model_id) in ModelGroup.QWEN:
                self.terminators = None
            else:
                self.terminators = [
                    self.tokenizer.eos_token_id,
                    self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
                ]

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id, 
                torch_dtype=torch.bfloat16,
                load_in_8bit=True,
                cache_dir=self.cache_dir, 
                device_map="auto"
                # device_map={"": "cuda:0"}
            )

            for module in self.model.children():
                print(module)

            # for 3.1 8B INT8
            self.generation_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
            )

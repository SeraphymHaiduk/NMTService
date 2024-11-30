from src.translation import Translator
from src.llm import LlmManager, LlamaWorker, AllowedModelID
class StartupManager:

  @staticmethod
  def load():
    StartupManager._translation_startup()
    StartupManager._llm_startup()

  @staticmethod
  def _translation_startup():
    Translator()

  @staticmethod
  def _llm_startup():
    LlmManager().create_process(LlamaWorker, AllowedModelID.LLAMA_8B_8INT_INSTRUCT.value)
from src.translation import Translator
class StartupManager:

  @staticmethod
  def load():
    StartupManager.translation_startup()

  @staticmethod
  def translation_startup():
    Translator()
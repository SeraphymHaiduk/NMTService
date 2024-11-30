from src.types.llm_chat import ChatMessageModel, ChatModel, ChatRole
from typing import NoReturn
users = [
    {
        "user_id": "aboba",
        "llm_chats": [
        ChatModel(chat_id="Flowers", messages=[
            ChatMessageModel(role=ChatRole.USER, content="Write me a poem about the flowers").model_dump(),
            ChatMessageModel(role=ChatRole.SYSTEM, content="""\
Dancing in the morning light.
Whispered hues, a fleeting hour,
Life's brief beauty, blooming flower.""").model_dump()
        ]).model_dump(),
        ChatModel(chat_id="Today's day", messages=[
            ChatMessageModel(role=ChatRole.USER, content="What is the day today?").model_dump(),
            ChatMessageModel(role=ChatRole.SYSTEM, content="""I can't answer to your question, so as I don't have functionality to get actual date""").model_dump()
        ]).model_dump(),
        ChatModel(chat_id="Winter outfit", messages=[
            ChatMessageModel(role=ChatRole.USER, content="write a short set of clothes for a winter").model_dump(),
            ChatMessageModel(role=ChatRole.SYSTEM, content="""\
Here's a simple winter outfit idea:\
Top: A thermal base layer under a cozy wool or cashmere sweater.\
Bottoms: Insulated jeans or thermal-lined leggings.\
Outerwear: A down-filled puffer jacket or a wool coat.\
Footwear: Waterproof snow boots with warm lining.\
Accessories: A knit scarf, a beanie, and touch-screen-compatible gloves.\
Extras: Thick wool socks and a layer of fleece-lined tights if it's very cold.\
Would you like style tips or specific color suggestions?\
""").model_dump()
        ]).model_dump()
        ]
    }
]

class Users:
    @staticmethod
    def get_llm_chats(user_id: str) -> list[ChatModel]:
        user_llm_chats = next((user["llm_chats"] for user in users if user["user_id"] == user_id), None)
        return user_llm_chats 

    @staticmethod
    def get_llm_chat(user_id: str, chat_id: str) -> ChatModel:
        user_llm_chats = Users.get_llm_chats(user_id=user_id)
        chat = next((chat for chat in user_llm_chats if chat["chat_id"] == chat_id), None)
        return ChatModel.model_validate(chat) 
    
    @staticmethod
    def create_llm_chat(user_id: str, new_chat_id: str) -> NoReturn:
        Users.get_llm_chats(user_id=user_id).append(ChatModel(
            chat_id=new_chat_id,
            messages=[]
        ))

    @staticmethod
    def add_message_to_llm_chat(user_id: str, chat_id: str, content: ChatMessageModel):
        user_llm_chats = next((user["llm_chats"] for user in users if user["user_id"] == user_id), None)
        chat = next((chat for chat in user_llm_chats if chat["chat_id"] == chat_id), None)
        chat["messages"].append(content.model_dump())
        
from fastapi import APIRouter, Body, Query
from src.llm import LlmManager, LlamaWorker
from src.types.llm_chat import ChatMessageModel, ChatModel
from src.models.user import Users 
router = APIRouter()

# TODO: add chat history
@router.post("/chat-complete/", description="""TODO: add description in llm_router""")
async def generate_response(user_id: str, chat_id: str, content: str = Body(..., embed=True)) -> str:
    print(f"user: '{user_id}' sent to chat: '{chat_id}' message: \n{content}")
    # TODO: In chat-completion route replace "generate" with "chat" method and create separate route for simple generate
    generated_text = await LlmManager().get_worker('LlamaWorker_0').execute(
        method=LlamaWorker.chat_complete, 
        params=(user_id, chat_id, content)
    )
    print(f"LLM output: {generated_text}")
    return generated_text


@router.get("/load-user-chats-list", description="""TODO: add route description""")
async def load_user_chats_list(user_id: str) -> list[ChatModel]:
    
    # TODO: use some database provider instead
    chats = await LlmManager().get_worker('LlamaWorker_0').execute(
        method=LlamaWorker.get_llm_chats_mock,
        params=user_id
    )
    return chats


@router.get("/load-chat", description="""TODO: add description in llm_router""")
async def load_chat(user_id: str, chat_id: str) -> ChatModel:
    
    # TODO: use some database provider instead
    chat = await LlmManager().get_worker('LlamaWorker_0').execute(
        method=LlamaWorker.get_llm_chat_mock,
        params=(user_id, chat_id)
    )
    return chat
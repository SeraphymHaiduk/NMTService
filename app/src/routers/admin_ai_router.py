from fastapi import APIRouter, Body
from src.llm import LlmManager, LlamaWorker

router = APIRouter()


@router.post("/user-request", description="""TODO: add description for admin ai router""")
async def user_request(
    apikey: str = Body(..., embed=True),
    user_input: str = Body(..., embed=True)
    ) -> str:
    print(f"---------- user-request -------- \napikey: {apikey},\nuser_input: {user_input}")

    generated_text = LlmManager().get_worker('LlamaWorker_0').execute(
        method=LlamaWorker.chat_complete, 
        # TODO: Replace with pydantic type
        params=tuple((apikey, user_input))
    )
    print(generated_text)
    return generated_text

@router.post("/output-update", description="""TODO: add description for admin ai router""")
async def output_update(
    apikey: str = Body(..., embed=True),
    new_output: str = Body(..., embed=True)
) -> None:
    print(f"--------- output-update --------\napikey: {apikey},\nnew_output: {new_output}")
    generated_text = LlmManager().get_worker('LlamaWorker_0').execute(
        method=LlamaWorker.add_system_output, 
        # TODO: Replace with pydantic type
        params=tuple((apikey, new_output))
    )
    
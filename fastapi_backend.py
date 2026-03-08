from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from logic.app import get_graph
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AIMessage
import uuid

app = FastAPI()


class ChatRequest(BaseModel):
    messages: Optional[List[Dict]] = None
    session_id: Optional[str] = None
    resume: Optional[str] = None


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):

    graph = await get_graph()

    session_id = request.session_id or str(uuid.uuid4())

    async def generator():

        # -----------------------
        # RESUME EXECUTION
        # -----------------------
        if request.resume:

            async for event in graph.astream(
                Command(resume=request.resume),
                config={"configurable": {"thread_id": session_id}},
                stream_mode="updates",
            ):

                if "__interrupt__" in event:
                    interrupt_value = event["__interrupt__"][0].value

                    yield "__INTERRUPT__\n"
                    yield interrupt_value + "\n"
                    yield "__END_INTERRUPT__\n"
                    return

                for node_output in event.values():

                    if "messages" in node_output:
                        msg = node_output["messages"][-1]

                        if msg.type == "ai":
                            yield msg.content or ""

            return

        # -----------------------
        # NORMAL MESSAGE FLOW
        # -----------------------
        lc_messages = []

        if request.messages:
            for msg in request.messages:

                if msg["role"] == "user":
                    lc_messages.append(HumanMessage(content=msg["content"]))

                elif msg["role"] == "assistant":
                    lc_messages.append(AIMessage(content=msg["content"]))

        async for event in graph.astream(
            {"messages": lc_messages},
            config={"configurable": {"thread_id": session_id}},
            stream_mode="updates",
        ):

            if "__interrupt__" in event:

                interrupt_value = event["__interrupt__"][0].value

                yield "__INTERRUPT__\n"
                yield interrupt_value + "\n"
                yield "__END_INTERRUPT__\n"
                return

            for node_output in event.values():

                if "messages" in node_output:

                    msg = node_output["messages"][-1]

                    if msg.type == "ai":
                        yield msg.content or ""

    return StreamingResponse(generator(), media_type="text/plain")

###########previpus code without hitl*********

# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # from typing import List, Dict
# # from logic.app import run_model

# # app = FastAPI()

# # class ChatRequest(BaseModel):
# #     messages: List[Dict]  # full conversation


# # @app.post("/chat")
# # async def chat_endpoint(request: ChatRequest):
# #     result = await run_model(request.messages)
# #     return {"response": result}

# # # uvicorn fastapi_backend:app --reload

# # streaming ... 
# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from typing import List, Dict
# from logic.app import stream_model

# app = FastAPI()

# class ChatRequest(BaseModel):
#     messages: List[Dict]


# from fastapi.responses import StreamingResponse

# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):

#     async def generator():
#         async for chunk in stream_model(request.messages):
#             yield chunk.encode("utf-8")

#     return StreamingResponse(
#         generator(),
#         media_type="text/plain",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#         },
#     )

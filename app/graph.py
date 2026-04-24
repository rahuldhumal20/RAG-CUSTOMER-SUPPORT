from typing import TypedDict
from langgraph.graph import StateGraph

from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, MODEL_NAME
from app.retriever import retrieve_context
from app.hitl import escalate_to_human
from app.memory import get_memory_context, save_to_memory

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME
)

class AgentState(TypedDict):
    query: str
    context: str
    route: str
    response: str


def process_node(state):

    query=state["query"].lower()

    result=retrieve_context(query)

    context=result["context"]

    score=result["score"]


    if "password" in query or "account" in query:
        intent="account"

    elif "order" in query or "shipping" in query:
        intent="order"

    elif "refund" in query or "return" in query:
        intent="refund"

    elif "payment" in query or "deducted" in query:
        intent="payment"

    elif "arrive" in query or "delivery" in query:
        intent="order"

    else:
        intent="unknown"


    memory = get_memory_context()

    if intent=="unknown" and memory.strip()=="":
        return {
           "query":query,
           "context":context,
           "route":"hitl",
           "response":""
        }
    
    if score > 1.8 and memory.strip()=="":
        return {
            "query":query,
            "context":context,
            "route":"hitl",
            "response":""
        }

    return {
        "query":query,
        "context":context,
        "route":"answer",
        "response":""

    }

    
def answer_node(state):

    memory = get_memory_context()

    prompt = f"""
    You are a professional customer support assistant.

    Rules:
    - Answer ONLY using the provided context
    - Be clear and concise
    - If unsure, say you are not confident

    Previous Conversation:
    {memory}

    Context:
    {state['context']}

    Question:
    {state['query']}

    Answer:
    """

    try:
        result = llm.invoke(prompt)

        save_to_memory(
            state["query"],
            result.content
        )

        return {
            "response": result.content
        }

    except Exception as e:
        print(f"LLM Error: {e}")  # you can use logging later

        return {
            "response": "We are experiencing technical difficulties. Please try again later."
        }

def hitl_node(state):

    return {
      "response":escalate_to_human(
         state["query"]
      )
    }


def route_decision(state):
    return state["route"]


builder=StateGraph(AgentState)

builder.add_node(
 "process",
 process_node
)

builder.add_node(
 "answer",
 answer_node
)

builder.add_node(
 "hitl",
 hitl_node
)

builder.set_entry_point(
 "process"
)

builder.add_conditional_edges(
   "process",
   route_decision,
   {
      "answer":"answer",
      "hitl":"hitl"
   }
)

builder.set_finish_point("answer")
builder.set_finish_point("hitl")

app_graph=builder.compile()
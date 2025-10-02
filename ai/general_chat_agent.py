# # ai_agents/simple_agent.py

# from typing import List, Optional, TypedDict, Annotated
# from pydantic import BaseModel
# from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.graph import StateGraph, END

# # — Setup LLM —
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro-latest", temperature=0.7)

# # — Agent state type —
# class AgentState(TypedDict):
#     messages: Annotated[List[AnyMessage], list]
#     has_answered: bool
#     final_answer: Optional[str]

# # — Node functions —
# def analyze_node(state: AgentState):
#     # Agar pehle se answer hai, skip kar do
#     if state.get("has_answered"):
#         return {"has_answered": True}

#     # Build prompt from messages
#     msgs = state["messages"]
#     prompt = ""
#     for m in msgs:
#         if isinstance(m, HumanMessage):
#             prompt += f"User: {m.content}\n"
#         elif isinstance(m, AIMessage):
#             prompt += f"Agent: {m.content}\n"
#     prompt += "\nAnswer the above question in a helpful farming style."

#     resp = llm.invoke(prompt)
#     return {
#         "has_answered": True,
#         "final_answer": resp.content
#     }

# def answer_node(state: AgentState):
#     # This node will just return final answer
#     return {"final_answer": state.get("final_answer")}

# def decide_condition(state: AgentState) -> str:
#     if state.get("has_answered"):
#         return "answer_node"
#     else:
#         return END

# # — Build graph —
# workflow = StateGraph(AgentState)
# workflow.add_node("analyze_node", analyze_node)
# workflow.add_node("answer_node", answer_node)
# workflow.set_entry_point("analyze_node")
# workflow.add_conditional_edges(
#     "analyze_node",
#     decide_condition,
#     {"answer_node": "answer_node", END: END}
# )
# workflow.add_edge("answer_node", END)

# agent = workflow.compile()

# # — Injection point function you’ll call in FastAPI route —
# def simple_agent_run(messages: List[AnyMessage]) -> dict:
#     """
#     messages: list of HumanMessage / AIMessage objects (langchain-style)
#     Returns dict with keys: final_answer (str)
#     """
#     initial_state: AgentState = {
#         "messages": messages,
#         "has_answered": False,
#         "final_answer": None
#     }
#     result = agent.invoke(initial_state)
#     return {"final_answer": result.get("final_answer")}

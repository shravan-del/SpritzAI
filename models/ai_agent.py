from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage, trim_messages
from langchain_core.tools import tool, ToolException, InjectedToolArg
from langchain_core.runnables import RunnableConfig
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun, HumanInputRun
from langgraph.graph import StateGraph,START,END, add_messages, MessagesState
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from typing import Annotated, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import uuid
import operator
from IPython.display import Image, display
import os
from ionic_langchain.tool import IonicTool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

#state definition - specifies what type of information will flow between different nodes and edges in a graph
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

model = "gpt-3.5-turbo-1106"
temperature = 0.6
# openai_api_key = ('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')
llm = ChatOpenAI(model=model, temperature=temperature, openai_api_key=openai_api_key)

ionic_tool = IonicTool().tool()

ionic_tool.description = str(
    """
Ionic is an e-commerce shopping tool. Assistant uses the Ionic Commerce Shopping Tool to find, discover, and compare products from thousands of online retailers. Assistant should use the tool when the user is looking for a product recommendation or trying to find a specific product.

The user may specify the number of results, minimum price, and maximum price for which they want to see results.
Ionic Tool input is a comma-separated string of values:
  - query string (required, must not include commas)
  - number of results (default to 4, no more than 10)
  - minimum price in cents ($5 becomes 500)
  - maximum price in cents
For example, if looking for coffee beans between 5 and 10 dollars, the tool input would be `coffee beans, 5, 500, 1000`.

Return them as a markdown formatted list with each recommendation from tool results, being sure to include the full PDP URL. For example:

1. Product 1: [Price] -- link
2. Product 2: [Price] -- link
3. Product 3: [Price] -- link
4. Product 4: [Price] -- link
"""
)

tools = [ionic_tool]

prompt = hub.pull("hwchase17/openai-tools-agent")

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, tools=tools, handle_parsing_errors=True, verbose=True, max_iterations=5
)

# COMMENTED OUT PART WILL BE IMPLEMENTED AS THE RECOMMENDER IS DESIGNED
# FOR NOW IONIC TOOL WILL BE USED IN ORDER TO BENCHMARK ACCURACY AND USE IT FOR MVP(maybe)
#function to add a node to Langraph agent
# def run_llm(state: State):
#    messages = state['messages']
#    message = model.invoke(messages)
#    return {'messages': [message]}

#creates simple graph
# graph_builder = StateGraph(State)
# graph_builder.add_node("llm", run_llm)
# graph_builder.add_edge(START, "llm")
# graph_builder.add_edge("llm", END)

# graph = graph_builder.compile()
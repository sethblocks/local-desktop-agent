from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tools import tool
from tools import fs, gnome, internet, linux, roomba #Custom Tools

#Langgraph (Experimental Ver)
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

import time
llm = ChatOllama(
    model="qwen3:4b",
    top_k=20,
    top_p=0.95,
    temperature=0.6
    )
print("Starting Agent ", llm.model)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Solve the given task or problem autonomously, no user input or questions is allowed. Use problem solving when errors occur."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

tools = [
    fs.find_file, 
    fs.read, 
    fs.write, 
    fs.ls, 
    fs.mkdir,
    gnome.light_dark_theme, 
    gnome.wallpaper, 
    gnome.accent_color,
    internet.image_search,
    internet.text_search,
    internet.wget,
    linux.terminal,
    linux.open,
    roomba.drive
    ]
# For whatever reason this is NOT recommended agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

agent = create_react_agent(model=llm, tools=tools)
# No longer needed??? executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

prompt = input("Prompt: ")
start = time.time()
response = agent.invoke({"messages": prompt})
# Print the response
print(response["messages"][-1].content)
print("Time Used:", time.time() - start)
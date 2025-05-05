from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tools import tool
from tools import fs, gnome, internet, linux #Custom Tools
import time
llm = ChatOllama(
    model="qwen3:4b",
    top_k=20,
    top_p=0.95,
    temperature=0.6
    )
print("Starting Agent ", llm.model)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a reasoning agent with tools. Answer the question or complete the task using reasoning and tools given to you. You may need to reason to understand the prompt. You may need to problem solve some tasks when errors occur."),
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
    linux.open]
agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

prompt = input("Prompt: ")
start = time.time()
response = executor.invoke({"input": prompt})

# Print the response
print(response["output"])
print("Time Used:", time.time() - start)
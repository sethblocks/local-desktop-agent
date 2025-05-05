from duckduckgo_search import DDGS
import subprocess
from langchain_core.tools import tool
from pathlib import Path
import cloudscraper
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


@tool
def tilde(directory: str):
    """Converts ~/ to /home/user/"""
    return directory.replace("~/", str(Path.home()) + "/")

@tool
def image_search(query: str):
        """Searches the internet for images"""
    #try:
        results = DDGS().images(query, size="Wallpaper", max_results=5)
        output = ""
        i=0
        for result in results:
            i+=1
            #print(result)
            output += "\n\nImage #" + str(i) + ":\nTitle: " + result['title'] + "\nURL: " + result['image']
        return output[2:]
    #except:
        return "Unable to access internet!"

@tool
def text_search(query: str):
    """Searches the internet, you may need to try multiple queries to get complete details"""
    return ""
    try:
        results = DDGS().text(query, max_results=5)
        output = ""
        i=0
        for result in results:
            i+=1
            print(result)
            output += "\nResult #" + str(i) + ":\nTitle:" + result['title'] + "\nText:" + result['body']
        return output[2:]
    except:
        return "Unable to access internet!"

@tool
def better_text_search(query: str):
    """Searches the internet"""
    llm = ChatOllama(
        model="qwen3:4b",
        top_k=20,
        top_p=0.95,
        temperature=0.2
    )

    try:
        results = DDGS().text(query, max_results=5)
        output = ""
        i=0
        for result in results:
            i+=1

            scraper = cloudscraper.create_scraper()
            content = scraper.get(result['href']).text
            

            soup = BeautifulSoup(content)
            text = soup.text
            while text.find("\n\n") != -1:
                text = text.replace("\n\n", "\n")
            
            output += "\nResult #" + str(i) + ":\nTitle:" + result['title'] + "\nText:" + text
        return llm.invoke([
            SystemMessage("You will receive search results. Clean up and return the relevent info in a readable format."),
            HumanMessage(output[2:])
        ]).content.split("</think>")[-1]
    except:
        return "Unable to access internet!"

@tool
def faster_text_search(query: str):
    """Searches the internet, really fast"""
    llm = ChatOllama(
        model="qwen3:1.7b",
        top_k=20,
        top_p=0.95,
        temperature=0.1
    )

    try:
        results = DDGS().text(query, max_results=3)
        output = ""
        i=0
        for result in results:
            i+=1

            scraper = cloudscraper.create_scraper()
            content = scraper.get(result['href']).text
            

            soup = BeautifulSoup(content)
            text = soup.text
            while text.find("\n\n") != -1:
                text = text.replace("\n\n", "\n")
            
            output += "\nResult #" + str(i) + ":\nTitle:" + result['title'] + "\nText:" + text
        return llm.invoke([
            SystemMessage("You will format and clean the relevent search result information you are given."),
            HumanMessage(output[2:])
        ]).content.split("</think>")[-1]
    except:
        return "Unable to access internet!"

@tool
def wget(url: str, output: str):
    """Uses the Wget command, outputs to the specified file"""
    print(url)
    res = subprocess.run(["wget", url, "-O", tilde(output)], capture_output=True, text=True)
    if res.stdout + "\n" + res.stderr == "\n":
        return "Error, could not download"
    return res.stdout + "\n" + res.stderr

if __name__ == "__main__":
    print(better_text_search("Samsung S24 Specs"))
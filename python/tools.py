#Python file for all of the AI Agents tools

#imports
from langchain.tools import tool
import os
import json
import requests
import subprocess
import sys
from pathlib import Path 
import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from openrouter import OpenRouter
from ddgs import DDGS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
#Making the client for our specialized AI's
client = OpenRouter(
    api_key=os.getenv('HACK_CLUB_AI'),
    server_url="https://ai.hackclub.com/proxy/v1",
)

client2 = OpenAI(
    api_key=os.getenv('HACK_CLUB_AI'),
    base_url="https://ai.hackclub.com/proxy/v1",
)

#Tool for our AI Agent to read file contents through a file path
@tool("ReadFile")
def read_file(file_url: str) -> str:
    """Whenever User wants something from their computer, use this function to read that file, it accepts a file_url as a str which is the file path on the local computer, if user doesn't provide you it, ask them for it. Returns file's content"""
    try:
        if '.csv' in file_url or '.pdf' in file_url:
            return 'File not supported to read, try using python instead to analzye it, if that fails just tell user you cant do it'
        with open(file_url, 'r', encoding='utf-8', errors='ignore') as file:
            line_count = len(file.readlines())
            file.seek(0)
            content = file.read()
        if line_count < 50:
            return content
        else:
            return 'File too big use Run_Python tool instead'
    except FileNotFoundError as e:
        return 'File Not Found'

#Tool to let AI read entire folder's content, helpful for like categoriztion and etc..
@tool("ReadFolder")
def read_folder(folder: str) -> str:
    """Use this to read all files from a user's folder, they must provide a folder path, use whenever they ask you to read a folder from thier computer or something related to this"""
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        return 'Folder not found'
    
    contents = []
    for file in files:
            try:
                with open(fr'{folder}/{file}', 'r', encoding='utf-8', errors='ignore') as file_content:
                    contents.append({'file_name': file, 'content': file_content.read()})
            except PermissionError:
                contents.append({'file_name': file, 'content': 'File Permission Denied'})
    
    return contents

#This is a search tool that uses brave search to let our AI Agent get current information
@tool("search")
def search(query: str) -> str:
    """
    ONLY USE WHEN NEEDED, AND ONLY ONCE PER PROMPT
    Searches the web for current information. Never use specific dates; Instead of latest iphone 2024 it would be latest iphone

    Input:
        query (str): what to search

    Output:
        list of objects with:
        - title
        - description
        - url
    """
    try:
        response = requests.get(
            'https://search.hackclub.com/res/v1/web/search',
            params={'q': query, 'count': 1},
            headers={'Authorization': f'Bearer {os.getenv("BRAVE_SEARCH_API")}'}
        )
        data = response.json()
        cleaned_data = []

        for i in data['web']['results']:
            cleaned_data.append({'title':i['title'], 'url': i['url'], 'description':i['description']})

        return json.dumps(cleaned_data)
    
    except Exception as e:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No search results found for this query"
        return "\n".join(
            f"{i+1}. {r['title']}: {r['body']}"
            for i, r in enumerate(results)
        )
    
#Tool to allow the AI to run Python Commands; The AI Agent basically has infinite possibilites with this
@tool("Run_Python")
def run_python(filecontent: str) -> str:
    """Runs python command based on what you write you could use this to analzye a datset a user provides you, or doing calculations, and etc. Whatever runs the user can see, like if you run a turtle python gui, the user will be able to see the turtle gui window, or see a plot and etc. DONT USE EMOJIS IN THE CODE"""
    files = Path('ai_python.py')
    files.write_text(filecontent,encoding='utf-8')
    result = subprocess.run([sys.executable, 'ai_python.py'], capture_output=True, text=True, timeout=100)

    output = result.stdout
    errors = result.stderr

    os.remove('ai_python.py')

    return output,errors

#Specialized AI for coding
@tool('coding')
def coding(prompt: str) -> str:
    """
    Use this for ANY coding task that is more than a one-liner.
    This includes: generating full scripts or functions, debugging errors,
    refactoring or improving existing code, building algorithms, explaining
    complex code, writing multi-step programs, or any language-specific task.
    Always prefer this over answering code questions yourself.
    Pass the full user request + any relevant code or context in the prompt.
    """
    response = client.chat.send(
        model="poolside/laguna-xs.2:free",
        messages=[
            {"role": "system", "content": "Be concise. No unnecessary explanation."},
            {"role": "user", "content": prompt}
        ],
    )
    return 'The Tool returned: ' + response.choices[0].message.content

#Specialized AI for reasoning tasks
@tool('reasoning')
def reasoning(prompt: str) -> str:
    """
    Use this for ANY task requiring deep thinking, multi-step logic, or accuracy.
    This includes: math problems, scientific questions, research summaries,
    fact-based analysis, comparisons, decision making, step-by-step reasoning,
    or any question where being correct matters more than being creative.
    Always prefer this over answering complex questions yourself.
    Pass the full user question + any gathered context in the prompt.
    """
    response = client.chat.send(
        model="openai/gpt-oss-120b:free",
        messages=[
            {"role": "system", "content": "Be concise. No unnecessary explanation."},
            {"role": "user", "content": prompt}
        ],
    )
    return 'The Tool returned: ' + response.choices[0].message.content

#Specialized AI for creative tasks, like writing a story
@tool('creative')
def creative(prompt: str) -> str:
    """
    Use this for ANY creative or imaginative writing task.
    This includes: fiction writing, short stories, roleplay, world building,
    character creation, dialogue, poetry, brainstorming creative ideas,
    writing in a specific style or tone, or any task where imagination matters.
    Always prefer this over writing creative content yourself.
    Pass the full user request + any style/tone/context details in the prompt. 'Use this tool
    """
    response = client.chat.send(
        model="z-ai/glm-4.5-air:free",
        messages=[
            {"role": "system", "content": "Be concise. No unnecessary explanation."},
            {"role": "user", "content": prompt}
        ],
    )
    return 'The Tool returned: ' + response.choices[0].message.content

#AI tool to allow our Agent to see!
@tool('vision')
def vision(prompt, file_path) -> str:
    """
    Use this whenever the user provides or references an image, chart, diagram,
    screenshot, document scan, or any visual content that needs to be understood.
    This includes: describing images, reading text from screenshots, analyzing
    charts or graphs, identifying objects, or answering questions about visual data.
    Always use this instead of trying to interpret visual content yourself.
    Pass the image file path + the user's question.
    """

    content = [{"type": "text", "text": prompt}]
    
    resolved_file_path = Path(file_path).resolve()
    if file_path:
        with open(resolved_file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = file_path.split(".")[-1].lower()

        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/{ext};base64,{b64}"}
        })
        

    response = ChatOpenAI(
        model="nvidia/nemotron-nano-12b-v2-vl:free",
        api_key=os.getenv('HACK_CLUB_AI'),
        base_url="https://ai.hackclub.com/proxy/v1"
    )

    result = response.invoke([HumanMessage(content=content)]).content
    if resolved_file_path and os.path.exists(file_path):
        os.remove(resolved_file_path)
    return 'The Vision Tool returned: ' + result   

#Now the AI Agent can generate images!
@tool('generate_image')
def generate_image(image_prompt: str) -> str:
    """Use this whenever you need to generate an image, user will be able to see the image + image will be saved as image.jpg, takes image prompt as the only input"""
    global image_created
    image_name = 'image.jpg'

    try:
        response = client2.chat.completions.create(
            model="google/gemini-3.1-flash-image-preview",
            messages=[
                {"role": "user", "content": image_prompt}
            ],
            extra_body={
                "modalities": ["image", "text"],
                "image_config": {"aspect_ratio": "16:9"}
            }
        )
    except Exception as e:
        return f"Image generation failed with error : {e}"

    try:
        image_url = response.choices[0].message.images[0]["image_url"]["url"]
    except (AttributeError, IndexError, TypeError, KeyError):
        return f"Image generation failed: Unexpected response structure."

    base64_data = image_url.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    with open(image_name, "wb") as f:
        f.write(image_bytes)

    image_created = True
    return 'Image successfully saved as image.jpg and will be visible to user'

#tool list and image created variable to let our UI know if it needs to diplay the generated image or not
image_created = False
tools_list = [read_file, read_folder, search, run_python, creative, reasoning, coding, vision, generate_image]

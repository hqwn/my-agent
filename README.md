# My-Agent

My very own AI agent, built using OpenRouter through a **Hackclub** proxy. It includes multiple tools to make it really agentic. Some include a search tool, a file reading tool, a tool to let it run Python code, and an image generation tool. It has even more features; scroll down to see all of them. 

Right now, if you want to clone it and run it, you won't be able to unless you are a Hack Club member, but I will be making it public in the future by making it use OpenRouter directly rather than using the Hack Club proxy. 

<details><summary>Click here to see more information about Hack Club</summary>

> If you are wondering what Hack Club is, it's a non-profit organization that provides free resources and support for high school coding clubs around the world and regularly hosts hackathons/online programs. They also provide a proxy for OpenRouter with $3 of credit per day, which is what I used to build this agent. They also provide a Brave search api key for free, which is what I used for the search tool. If you are interested in joining Hack Club, you can check out their website [here](https://hackclub.com/).

</details>


<details><summary>Disclaimer:</summary>

> This project was more of a learning experience for me; admittedly, it does have some kinks and bugs, but the main structure is there. Please feel free to contribute and make it better, or if you have any suggestions, please let me know.

</details>

<br>

## Image of the project

![UI image](images/vision.png)


## Features/tools

The AI agent is built using Python and LangChain. The main way I made it agentic is by giving it multiple tools. Making it **WAY** smarter and more capable. Before I list all the tools, I want to tell you that the agent isn't just 1 AI, but **6**! Why? Well, the main AI (GPT -20 b is really good for general tasks and calling tools, but not for specific needs which the user might need. For this exact reason, I included 5 other AI's, which are:

- **poolside/laguna-xs.2:free**: for coding tasks, it has the best balance between speed and good code, + it's free

- **openai/gpt-oss-120b: free**: for reasoning tasks, from my testing, it's the best free model for reasoning

- **z-ai/glm-4.5-ai r: free**: for creative tasks, it's the best free model for creative tasks, like writing stories, poems, etc

- **nvidia/nemotron-nano-12b-v2-vl:free**: for vision tasks; first vision AI I found 😅

- **google/gemini-3.1-flash-image-preview**: for image generation; this is the only paid model because there are NO free AI generation models on OpenRouter. It's the cheapest/best image generation model I found on OpenRouter, so I went with it.

That concludes the different AI's the agent can use; now let's get into the tools aat itsdisposal it can use:


- **Search**: Pretty self-explanatory, searches the web; It uses the Brave search API, but if that isn't working for some reason, it automatically switches to DuckDuckGo search, which is free.

- **Read File**: It can read files if the user uploads a path to a file; if the file is too large, it uses the Python tool to analyze the file in chunks.

- **Read Folder**: It can read folders and see what files are in them, which is really useful for the agent to see the files/seperation of folders and files in a user's project. Only works if the user provides the folder path/

- **Python Tool**: It can run Python code, which is really useful for doing calculations, analyzing data, or even just running code that the user gives it. This basically makes the agent able to do anything Python can do, which is a lot of things.


That concludes the list of tools the agent can use; now let's talk about the project's UI. The project uses **Streamlit** for the UI. You can upload files and talk to the agent all through the UI. 

Now, finally, let's talk about the agent's system prompt. The system prompt is carefully crafted using me/claude/and random smart engineers on the internet. The system prompt basically tells the agent about the tools it has and how to use them. It also tells the agent not to overcomplicate code. Like, if the user asks it to write a function that adds 2 numbers, it shouldn't write 100 lines of code with classes and stuff, but rather a simple function that adds 2 numbers. The system prompt also tells the agent to use different AI's for different tasks, which I mentioned earlier.



---

#Setting up right now is only for Hack Club members

## (First way of setting up; recommended) Setting Up Using the Release 

You can set up the Agent using 2 ways: the release way or by cloning the repo. If you don't want to clone the repository, install Python, or deal with terminal dependencies, you can download the release .exe file by itself.

### 1. Download the package
* Go to the [Latest Releases Page](https://github.com/hqwn/my-agent/releases/tag/v1.0.1).
* Go to the **Assets** section and download the compressed zip called: `my-agent.zip`.

### 2. Extract the Files
* Go to the `my-agent.zip` file on your computer that you just downloaded, and extract all the contents.
> **Important:** Extract the folder before running the .exe

### 3. Fill in your .env

1. Open the extracted folder.
2. Find the **`.env.example`** file by the .exe.
3. Rename it to **`.env`** with nothing in front or after, exactly **`.env`**.
4. Open the **`.env`** file and fill in your Hack Club API keys:
   * **HACK_CLUB_AI:** Paste your key from [ai.hackclub.com](https://ai.hackclub.com/)
   * **BRAVE_SEARCH_API_KEY (Optional):** Paste your key from [search.hackclub.com](https://search.hackclub.com/) (If you dont fill this out, it automatically switches to DuckDuckGoSearch).

### 4. Run the Agent
* Double-click the **`my-agent.exe`** file.
* Then the file will automatically open up the streamlit UI at `http://localhost:8501`

## (Second way of setting it up) Setting it up by cloning the repo 

1. Clone the repo and go into it

```bash
git clone https://github.com/hqwn/my-agent
cd my-agent
```

2. Install all of the requirements

```bash
pip install -r requirements.txt
```

3. Copy the .env.example to .env after going into the python folder and fill out your API keys, code below, along with how to get API key

- AI API key: https://ai.hackclub.com/

- Brave Search API key: https://search.hackclub.com/

```bash
cd python
copy .env.example .env
```

REMEMBER TO FILL IN THE API KEYS IN THE .env FILE (AI API key required, but BRAVE SEARCH API key isn't required; If you don't fill the Brave Search Api key, it just uses DuckDuckGo Search, which doesn't need an API key)

4. Run the project

```bash
python -m streamlit run ui.py
```

## Links

- YouTube Channel: https://www.youtube.com/@RuCode

- LinkedIn: https://www.linkedin.com/in/aryan-jain-085401344/

- Gmail: aryanjain9818@gmail.com

- More Projects: Check my GitHub profile

## More Images

![UI image](images/ui.png)
![vision image](images/vision.png)
![image generation image](images/image.png)

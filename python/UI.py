#Python file for the main UI (using streamlit)

#Imports
import streamlit as st
from main import ask_streamlit
import tools
import pandas as pd

st.title('Your Chat Bot')

#A function to be able to save a file, using a file extension, and the raw file
def save_file(file_extension, file):
    with open(f'file.{file_extension}', 'wb') as f:
        f.write(file.getvalue())
    return f'file.{file_extension}'

#Chat history and our AI Agent history setup
if 'chat_history' not in st.session_state or 'agent_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.agent_history = []

#Assigning the history to a variable for easier use 
history = st.session_state.chat_history
a_history = st.session_state.agent_history

#Showing all messages
for message in history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Chatting UI

#self-explanitory, asking for user's prompt
prompt = st.chat_input("Type your message...", accept_file=True, accept_audio=True)
if prompt:

    #Appending the users message to chat history + initalizing variables
    file_link = None
    history.append({'role':'user', 'content':prompt.text})

    #Writing the users message
    with st.chat_message("user"):
    
        #Writing the user's text if the wrote anything
        if prompt.text is not None:
            st.write(prompt.text)

        #Logic for displaying file if file uploaded
        if prompt['files'] != []:
            #Figuring out file type
            if 'image' in prompt.files[0].type:
                #If user's file is an image, we display it and save the file, then give the agent the file path, to let it use the vision tool to analyze it if it wants
                st.image(prompt.files[0])
                file_link = save_file(prompt.files[0].name.split('.')[1], prompt.files[0])
                a_history.append({"role": "user","content": prompt.text +f" The user added a image file who's path is {file_link}, use the vision tool to analzye image"})
            elif 'csv' in prompt.files[0].type:
                #This is the only reason I have the pandas library, to read a csv/xlsx file if the user added one
                st.dataframe(pd.read_csv(prompt.files[0]))
                file_link = save_file(prompt.files[0].name.split('.')[1], prompt.files[0])
                a_history.append({"role": "user","content": prompt.text +f" The user added a csv/xlsx file who's path is {file_link}"})
            elif 'json' in prompt.files[0].type:
                #Again displaying and saving a json file, if user adds one
                st.json(prompt.files[0])
                file_link = save_file(prompt.files[0].name.split('.')[1], prompt.files[0])
                a_history.append({"role": "user","content": prompt.text +f" The user added a csv/xlsx file who's path is {file_link}"})
        else:
            #We just add the text from the user if they didn't include a file
            a_history.append({"role":"user", "content": prompt.text if prompt.text else 'User provided nothing'})

    with st.chat_message("assistant"):
        #Displaying AI Agent's response

        #Creating a placeholder for our message
        message_placeholder = st.empty()

        try:

            #Showing the spinner while the Agent is thinking, so the user doesn't think the agent is broken
            with st.spinner("Thinking..."):
                result = ask_streamlit(a_history)

            # Show assistant message

            #Basically all the code does under this, is just show a generated image, if user generated an image
            if tools.image_created:
                st.image('image.jpg', 'Your generated Image, right click to download')
                with open("image.jpg", "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name="generated_image.jpg",
                        mime="image/jpeg"
                    )
                tools.image_created = False
            
            #Now we replace the placeholder with the actual AI agent's result
            message_placeholder.markdown(result)

            # Saving the agent's reponse to the agent's history
            history.append({
                "role": "assistant",
                "content": result
            })
            a_history.append({
                "role": "assistant",
                "content": result
            })

        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            message_placeholder.error(error_msg)

            history.append({
                "role": "assistant",
                "content": error_msg
            })
            a_history.append({
                "role": "assistant",
                "content": error_msg
            })
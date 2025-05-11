from customtkinter import *
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.0-flash")

app = CTk()
app.geometry("960x550")
app.title("Gemini AI Chat")

chat_history = []

def send_message():
    user_text = entry.get()
    if not user_text.strip():
        return  

    entry.delete(0, END)  

    response = chat.send_message_stream(user_text)
    ai_response = "".join(chunk.text for chunk in response)  

    chat_history.append({"User": user_text, "AI": ai_response})

    text_area.insert(END, f"You: {user_text}\n", "user")
    text_area.insert(END, f"AI: {ai_response}\n", "ai")
    text_area.insert(END, "-"*40 + "\n" + "\n")

text_area = CTkTextbox(app, wrap="word", width=920, height=450, font=("Roboto", 16))
text_area.pack(pady=10)

entry = CTkEntry(app, width=400, font=("Roboto", 14))
entry.pack(pady=10)
entry.bind("<Return>", lambda event: send_message())  

app.mainloop()

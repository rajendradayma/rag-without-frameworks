import chainlit as cl
import requests
import os


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

@cl.on_chat_start
async def welcome():
    await cl.Message("👋 Welcome to PDF-RAG! Upload a PDF using the 📎 (paperclip) button, then ask questions about its content.").send()

@cl.on_message
async def handle_message(message):
    # File upload handling
    if message.elements:
        for element in message.elements:
            if element.mime == "application/pdf":
                with open(element.path, "rb") as f:
                    files = {"pdf": (element.name, f, "application/pdf")}
                    try:
                        resp = requests.post(f"{BACKEND_URL}/upload_pdf/", files=files)
                        data = resp.json()
                        if resp.status_code == 200 and data.get('status') == 'success':
                            await cl.Message(f"✅ PDF '{element.name}' uploaded and indexed! Now type a question.").send()
                        else:
                            await cl.Message(f"❌ Upload failed: {data}").send()
                    except Exception as e:
                        await cl.Message(f"❌ Error uploading PDF: {str(e)}").send()
                return

    # Regular text question
    payload = {"question": message.content}
    try:
        resp = requests.post(f"{BACKEND_URL}/ask/", data=payload)
        data = resp.json()
        answer = data.get('answer', 'No answer returned.')
        context = data.get('retrieved_context', [])
        display = answer
        if context and isinstance(context, list) and "No relevant data" not in context[0]:
            display += "\n\n---\n_Context used:_\n" + "\n---\n".join(context)
        await cl.Message(display).send()
    except Exception as e:
        await cl.Message(f"❌ Error communicating with backend: {str(e)}").send()

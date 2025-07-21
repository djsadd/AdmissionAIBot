import openai
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from openai import AsyncOpenAI


assistant_id = "asst_QJ8zunURJ4GFgTMewnwCDdsj"
thread = openai.beta.threads.create()
openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Привет, мой агент!"
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def ask_gpt(prompt: str) -> str:
    try:
        # 1. Создаем thread
        thread = await client.beta.threads.create()

        # 2. Отправляем сообщение
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # 3. Запускаем ассистента
        run = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # 4. Ждем завершения
        while True:
            run_status = await client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                return "Ассистент не смог завершить выполнение."
            await asyncio.sleep(1)

        # 5. Получаем ответ
        messages = await client.beta.threads.messages.list(thread_id=thread.id)

        for message in reversed(messages.data):
            if message.role == "assistant":
                return message.content[0].text.value.strip()

        return "Ассистент не дал ответа."

    except Exception as e:
        return f"Произошла ошибка: {e}"
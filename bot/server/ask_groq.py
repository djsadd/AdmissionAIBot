import json
from docx import Document
import os
# Models

from services.groq_service import ask_groq, ask_groq_category

from db.crud import save_chat_history, get_history_text_by_session


files = {
    "Грант ректора": "Грант ректора.docx",
    "Контактная информация": "контактная информация.docx",
    "Международные программы": "Международжные программы.docx",
    "Документы для бакалавриата после колледжа(ускоренники)": "Необходимые документы бакалавр после колледжа.docx",
    "Документы для бакалавриата после школы": "Необходимые документы бакалавр после школы.docx",
    "Документы для магистратуры": "Необходимые документы магистратуры.docx",
    "Образовательные программы": "Образовательные программы.docx",
    "Общежитие": "общежитие.docx",
    "Проходные баллы ЕНТ для бакалавриата после школы": "Проходные баллы ЕНТ Бакалавриат.docx",
    "скидки на обучения": "скидки на обучение.docx",
    "студенческие организации": "Студенческие организации ТАУ.docx",
    "Цены на обучение": "Цены.docx",
    "Творческие экзамены": "творческие экзамены.docx",
    "сроки обучения": "Сроки обучения.docx",
    "Как подписать договор в Platonus с помощью ЭЦП": "Договор.docx",
}


async def ask_ai(query, uuid, platform="Telegram"):
    session_id = uuid
    history_text = await get_history_text_by_session(session_id)
    categories = await categorize_query(query, history_text)
    if categories == "⚠️ Пустой ответ от ИИ" or categories == "⚠️ Не удалось распарсить JSON":
        return "🧠 Ответ от ИИ:\n" + "Не удалось выполнить запрос, попробуйте еще раз"
    elif categories == "Бот не знает ответа на вопрос касательно приемной комиссии":
        return "🧠 Ответ от ИИ:\n" + "К сожалению я не обладаю такой информацией"
    else:

        response = await ask_groq(history_text, query, categories)
        if response.strip():
            try:
                parsed_response = json.loads(response)
                print(parsed_response)

                answer_value = parsed_response["answer"]
                await save_chat_history(session_id=session_id, query=query, response="Бот не знает ответа на вопрос касательно приемной комиссии",
                                        platform="Telegram")
                if answer_value == "Нет ответа":
                    return "К сожалению я не обладаю такой информацией"

                answer_value = parsed_response["answer"]
                await save_chat_history(session_id=session_id, query=query, response=answer_value,
                                        platform="Telegram")
                return answer_value
            except:
                return response.strip()
        await save_chat_history(session_id=session_id, query=query, response=response, platform=platform)
        return response


async def categorize_query(query, history_text):
    response = await ask_groq_category(query, history_text)
    if response.strip():
        try:
            parsed_response = json.loads(response)

            category = parsed_response.get("category", {})
            data = ""

            for title_key, value in category.items():
                file_path = f"C:\\Users\\admin\\PycharmProjects\\AIChatBot-Admission\\bot\\services\\info\\{files[value]}"

                if os.path.exists(file_path):
                    doc = Document(file_path)
                    text = '\n'.join([para.text for para in doc.paragraphs])
                    data += text
                    data += "\n"
                else:
                    print(f"Файл не найден: {file_path}")  # или можно логировать ошибку
            return data

        except json.JSONDecodeError as e:
            return response
        except KeyError as e:
            return response
        except AttributeError as e:
            return response
    else:
        return response

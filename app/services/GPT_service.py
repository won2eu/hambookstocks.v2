import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
GPT_KEY = os.environ.get("GPT_KEY")
client = openai.OpenAI(api_key=GPT_KEY)


def summarize_news(news_json):
    news_list = json.loads(news_json)

    for news in news_list:
        news["본문"] = gpt_answer(news["본문"])

    return news_list


def gpt_answer(news):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "헤드라인에 쓸건데 자극적으로 제목 없이 2줄 요약 해줘",
                },
                {"role": "user", "content": news},
            ],
            max_tokens=3000,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return "요약 실패"

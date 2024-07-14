from openai import OpenAI
import json

API_KEY = "API key"


def read_json(file):
    with open(file) as f:
        return json.load(f)



def write_txt(file, data):
    with open(file, "a") as f:
        f.write(f"{data},\n")



def get_chat_respnose_long_discription(client, cards, response):
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
             {
                "role": "system",
                "content": "You are expert in deciphering the meaning of Tarot readings and you use Russian language to write it."
            },
            {
                "role": "user",
                "content": f"As input you get responce: <response from user>, layout: <layout of Tarot's cards>. As output you write your deciphering.\
                language: Russian,\
                Input:\
                    Response:{response},\
                    Cards: {cards}",
            },
        ],
    )
    print(completion.usage.total_tokens)
    return completion.choices[0].message.content

def get_chat_respnose_short_discription(client, cards, response):
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
             {
                "role": "system",
                "content": "You are expert in deciphering the meaning of Tarot readings and you use Russian language to write it."
            },
            {
                "role": "user",
                "content": f"As input you get responce: <response from user>, layout: <layout of Tarot's cards>. As output you write your only summery about deciphering.\
                language: Russian,\
                Input:\
                    Response:{response},\
                    Cards: {cards}",
            },
        ],
    )
    print(completion.usage.total_tokens)
    return completion.choices[0].message.content


def deciphering(cards, responce, type):
    client = OpenAI(api_key=API_KEY)
    try:
        if type == 'Польное описание вместе с описанием карт':
            discription = get_chat_respnose_long_discription(client, cards ,responce)
        if type == 'Только трактовку расклада':
            discription = get_chat_respnose_short_discription(client, cards ,responce)
    except:
        discription = "Возникли проблемы в работе сервиса\
Подождите некоторое время, мы уже занимаемся решением данного вопроса"

    return discription.replace("*", "")

if __name__ == "__main__":
    deciphering()

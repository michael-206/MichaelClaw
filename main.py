import telebot
from openai import OpenAI
import json
from tools import tools
from skills.weather import get_current_weather, get_weather_forecast
from skills.transit import build_board
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

bot = telebot.TeleBot(os.getenv("TELEBOT_TOKEN"))

message_history=[{"role": "system", "content": "you are a digital secretary/assistant, like tony stark's Jarvis. be charismatic, Use quick and clever humor when appropriate. try to keep your responses short and efficient. feel free to use emojis, and feel free to crack a joke every now and then. as the user will interact with you most of the time verbaly, dont go on monologues. if the user asks for specific information, respond to the request but dont elaborate too much. if the user asks when the next transit vehicle leaves for a certain route, tell them the departures for that route, dont bore them with information that the user didnt ask for, apply this to all requests."}]

def ask_ai(prompt):
    # ----------------------------
    # 1. Ask the model something
    # ----------------------------
    print(tools)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        tools=tools
    )

    # ----------------------------
    # 2. Handle tool calls
    # ----------------------------
    output_messages = []

    for item in response.output:
        if item.type == "function_call":
            name = item.name
            args = json.loads(item.arguments)
            print(f"Using tool: {name}")
            if name == "get_current_weather":
                result = get_current_weather(args["location"])

                # Send tool result back to model
                output_messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })
            if name == "get_weather_forecast":
                result = get_weather_forecast(args["location"], args["days"])

                # Send tool result back to model
                output_messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })
            if name == "get_nearby_departures":
                result = build_board(args["location"], args["radius"])
                print(result)
                # Send tool result back to model
                output_messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })


    # ----------------------------
    # 3. Ask model again with tool results
    # ----------------------------
    final_response = client.responses.create(
        model="gpt-4.1-mini",
        input=str(prompt) + str(response.output) + str(output_messages)
    )

    print(final_response.output_text)
    message_history.append({"role": "assistant", "content": final_response.output_text})
    return final_response.output_text

@bot.message_handler(commands=['health','healthcheck'])
def send_hello(message):
    print(message)
    bot.send_message(message.from_user.id, "Health: OK")

@bot.message_handler(commands=["clear","clear_memory"])
def clear_chat(message):
    message_history = []
    bot.send_message(message.from_user.id, "Cleared Memory")

@bot.message_handler()
def echo_all(message):
    message_history.append({"role": "user", "content": message.text})
    bot.send_message(message.from_user.id, ask_ai(message_history))

bot.infinity_polling()
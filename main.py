import random
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from datetime import datetime
from zoneinfo import ZoneInfo

import requests

import re

import math

load_dotenv()



SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

@app.command("/ultima-hello")
def handle_hello(ack,respond,body):
    ack()
    user_id = body["user_id"]
    respond(f"Hello <@{user_id}>! I am your *Slacking Ultima*, online and ready to assist. What you you like to do?")

@app.command("/ultima-ping")
def handle_ping(ack,respond):
    ack()
    respond("Pong!!! Ultima is active and responsive!")

@app.command("/ultima-roll")
def handle_roll(ack,respond):
    ack()
    result = random.randint(1,6)
    respond(f" Ultima rolled a die for you... You got a {result}!")


#Rock paper sissors game

CHOICES = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

@app.command("/ultima-rps")
def hangle_guess_who(ack,respond,body):
    ack()
    user_id = body["user_id"]
    
    respond(
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f" <@{user_id}> has challenged *Ultima* to a battle! Choose your move:"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "🪨 Rock"},
                        "value": "rock",
                        "action_id": "rps_rock"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "📄 Paper"},
                        "value": "paper",
                        "action_id": "rps_paper"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "✂️ Scissors"},
                        "value": "scissors",
                        "action_id": "rps_scissors"
                    }
                ]
            }
            
        ]
    )
@app.action(re.compile(r"^rps_"))
def handle_some_action(ack, body, respond):
    ack()
    user_choice = body["actions"][0]["value"]
    user_id = body["user"]["id"]
    
    bot_choice = random.choice(list(CHOICES.keys()))
    
    if user_choice == bot_choice:
        result = "Its a tie 🤝!!"
    elif (
        (user_choice == "rock" and bot_choice == "scissors") or
        (user_choice == "paper" and bot_choice == "rock") or
        (user_choice == "scissors" and bot_choice == "paper")
    ):
        result = f"🎉 <@{user_id}> *WON*!"
    else:
        result = ":pensive: Ultima Wins!!! Better luck next time!"
    
    respond(
        text=f"Game over!",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*Rock, Paper, Scissors Results*\n\n"
                        f"<@{user_id}> picked: {CHOICES[user_choice]} *{user_choice.capitalize()}*\n"
                        f"Ultima picked: {CHOICES[bot_choice]} *{bot_choice.capitalize()}*\n\n"
                        f"Result: {result}"
                    )
                }
            }
        ],
        replace_original=True
    )

@app.command("/ultima-joke")
def handle_joke(ack,respond):
    ack()
    try:
        response = requests.get("https://icanhazdadjoke.com/",headers={"Accept": "application/json"})
        if response.status_code == 200:
            joke = response.json()["joke"]
            respond(f"{joke} 😂")
        else:
            respond("The Ultima is kinda lacking right now :robot_face:")
    except Exception:
        respond("Ultima failed to get a joke :( ")


# A simple Calculator 


@app.command("/ultima-calc")
def handle_calc(ack,respond,command):
    ack()
    expr = command.get("text","").strip()
    if not expr:
        respond("Provide an expression! Example: `/ultima-calc 15 * 4.5`")
        return
    if len(expr) > 50:
        respond("⚠️ Expression is too long! Keep it under 50 characters.")
        return
    if "**" in expr or "^" in expr:
        respond("⚠️ Exponentiation (`**` or `^`) is disabled to prevent huge numbers.")
        return
    
  
    
    try:
        allowed = "0123456789+-*/(). "
            
        if not all(c in allowed for c in expr):
            respond("⚠️ Only basic math operators (`+`, `-`, `*`, `/`) are allowed.")
            return
        result = eval(expr)
        
       
        respond(f" *Calculation* :  {expr} = *{result}*")
    except ZeroDivisionError:
        respond("You can't divide by Zero!")
    except Exception:
        respond("Invalid maths expression!")


TimeZones= {
    "🇺🇸 US Pacific (SF / Seattle)": "America/Los_Angeles",
    "🇺🇸 US Eastern (NY / DC)": "America/New_York",
    "🇬🇧 UTC / UK (London)": "Europe/London",
    "🇪🇺 Central Europe (Berlin / Paris)": "Europe/Berlin",
    "🇮🇳 India (IST)": "Asia/Kolkata",
    "🇯🇵 Japan (Tokyo)": "Asia/Tokyo",
    "🇦🇺 Australia (Sydney)": "Australia/Sydney",
}

@app.command("/ultima-tz")
def handle_time(ack,respond):
    ack()
    
    lines = []
    for label, tz_str in TimeZones.items():
        now = datetime.now(ZoneInfo(tz_str))
        formatted_time = now.strftime("%I:%M %p %Z (%b %d)")
        lines.append(f"• *{label}:* `{formatted_time}`")
    
    respond(
        blocks = [
            {
            "type": "header",
            "text": {"type": "plain_text", "text": "🌍 Ultima Team World Clock"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "\n".join(lines)}
        }
        ]
    )
    
    
            
if __name__ == "__main__":
    print("⚡️ Ultima is starting up...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
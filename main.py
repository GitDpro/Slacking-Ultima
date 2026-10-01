import random
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()



SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

@app.command("/ultima-hello")
def handle_hello(ack,respond,body):
    ack()
    user_id = body["user_id"]
    respond(f"Hello <@{user_id}>! I am your ** Slacking Ultima**, online and ready to assist.")

@app.command("/ultima-ping")
def handle_ping(ack,respond):
    ack()
    respond("Pong!!! Ultima is active and responsive!")

@app.command("/ultima-roll")
def handle_roll(ack,respond):
    ack()
    result = random.randint(1,6)
    respond(f" Ultima rolled a die for you... You got a {result}!")
    
if __name__ == "__main__":
    print("⚡️ Ultima is starting up...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
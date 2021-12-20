from dotenv import load_dotenv
from datetime import datetime

from utils import get_env, env_vars, get_month, Venmo, Telegram

def main(now):
  """
  The main function which initiates the script.
  """

  load_dotenv()  # take environment variables from .env.
  actualVars = []
  for var in env_vars:
    actualVars.append(get_env(var))

  access_token, chat_id, bot_token = actualVars

  month = get_month(now)
  venmo = Venmo(access_token)
  telegram = Telegram(bot_token, chat_id)

  friends = [
    {
      "name": "Saumya",
      "user_name": "Saumya-Singhal",
      "amount": 1.00,
      "type": "send",
      "description": "Testing automated Venmo Payments"
    }
  ]

  successfulRequests = []
  expectedRequests = len(friends)

  for friend in friends:
    name = friend["name"]
    user_name = friend["user_name"]
    user_id = venmo.get_user_id_by_username(user_name)
    description = friend["description"] + " - for " + month
    amount = friend["amount"]
    message = "Good news!\n"
    message += "I have successfully sent money to " + name
    success = venmo.send_money(user_id, amount, description, telegram.send_message(message))
    if success:
      successfulRequests.append(success)

  if len(successfulRequests) == expectedRequests:
    print("✅ Ran script successfully and sent " + str(expectedRequests) + " Venmo requests.")
  else:
    print("❌ Something went wrong. Only sent " + str(len(successfulRequests)) + "/" + str(expectedRequests) + " venmo requests.")

now = datetime.now()
main(now)

from dotenv import load_dotenv
from datetime import datetime

from utils import get_env, env_vars, Venmo, Telegram, load_json

def main(now):
  """
  The main function which initiates the script.
  """

  load_dotenv()  # take environment variables from .env.
  actualVars = []
  for var in env_vars:
    actualVars.append(get_env(var))

  access_token, chat_id, bot_token = actualVars

  date = now.strftime("%B %d, %Y")
  time = now.strftime("%H:%M%p")
  telegram = Telegram(bot_token, chat_id)
  def dual_print(message):
    print(message)
    telegram.send_message(message)

  dual_print(f'🕘 Monthly Venmo payment scheduler running on {date} at {time}')

  scheduled_requests = load_json('data.json')

  sentRequests = []
  non_test_requests = list(filter(lambda r: r["test"] == False, scheduled_requests))
  expectedRealRequests = len(non_test_requests)

  for scheduled_request in scheduled_requests:
    name = scheduled_request["name"]
    user_name = scheduled_request["user_name"]
    description = f'{scheduled_request["description"]} for {date} at {time}'
    amount = scheduled_request["amount"]
    message = "Good news!\n"
    message += "I have successfully sent money to " + name
    if scheduled_request["test"] == True:
      dual_print("Testing scheduled message to " + name)
    else:
      venmo = Venmo(access_token)
      user_id = venmo.get_user_id_by_username(user_name)
      success = venmo.send_money(user_id, amount, description, dual_print(message))
      if success:
        sentRequests.append(success)

  if len(sentRequests) == expectedRealRequests:
    dual_print("✅ Ran script successfully and sent " + str(expectedRealRequests) + " actual Venmo requests")
  else:
    dual_print("❌ Something went wrong. Only sent " + str(len(sentRequests)) + "/" + str(expectedRealRequests) + " venmo requests.")

now = datetime.now()
main(now)

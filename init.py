from dotenv import load_dotenv
from datetime import datetime
import argparse

from utils import get_env, env_vars, Venmo, Telegram, load_json
import json
import base64

# Set Parameters
parser = argparse.ArgumentParser(description='Sends Venmo payments/requests.')
parser.add_argument('--type', help='Script type: ENUM(monthly bi_yearly)', default='monthly')
parser.add_argument('--env', help='Script type: ENUM(development production)', default='development')

def main(now):
  """
  The main function which initiates the script.
  """

  load_dotenv()  # take environment variables from .env.
  actualVars = []
  for var in env_vars:
    actualVars.append(get_env(var))

  access_token, chat_id, bot_token, user_encoded_data = actualVars

  date = now.strftime("%B %d, %Y")
  time = now.strftime("%H:%M%p")
  telegram = Telegram(bot_token, chat_id)
  def dual_print(message):
    print(message)
    telegram.send_message(message)

  args = parser.parse_args()
  script_type = args.type
  script_env = args.env
  development_environment = script_env == "development"
  # We pull data down from USER_JSON_STRING_DATA secret stored in Github
  # It is base64 encoded so we need to decode it and then load it as json
  user_json_string_data = base64.b64decode(user_encoded_data)
  dual_print("user_json_string_data + " + user_json_string_data)
  scheduled_requests = json.loads(user_json_string_data)
  # dual_print(scheduled_requests)

  script_type_as_english = "Monthly" if script_type == "monthly" else "Bi-Yearly"
  dual_print(f'🕘 {script_type_as_english} Venmo payment scheduler running on {date} at {time}')

  sentRequests = []
  expectedRequests = len(scheduled_requests)

  # for scheduled_request in scheduled_requests:
  #   name = scheduled_request["name"]
  #   print("name + " + name)
  #   user_name = scheduled_request["user_name"]
  #   print("user_name + " + user_name)
  #   description = f'{scheduled_request["description"]} for {date} at {time}'
  #   amount = scheduled_request["amount"]
  #   message = "Good news!\n"
  #   message += "I have successfully sent money to " + name
  #   if development_environment:
  #     dual_print("Testing scheduled message to " + name)
  #   else:
  #     venmo = Venmo(access_token)
  #     user_id = venmo.get_user_id_by_username(user_name)
  #     success = venmo.send_money(user_id, amount, description, dual_print(message))
  #     if success:
  #       sentRequests.append(success)

  if development_environment:
    dual_print(f'✅ Ran script successfully and tested {expectedRequests} Venmo requests')
  elif len(sentRequests) == expectedRequests:
    dual_print(f'✅ Ran script successfully and sent {expectedRequests} actual Venmo requests')
  else:
    dual_print(f'❌ Something went wrong. Only sent {len(sentRequests)} / {expectedRequests} venmo requests.')

now = datetime.now()
main(now)

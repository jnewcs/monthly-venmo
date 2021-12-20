from datetime import datetime

from utils import verify_env_vars, env_vars, get_env_vars, Telegram, Venmo
from dotenv import load_dotenv

def main(now):
  load_dotenv()
  date = now.strftime("%B %d, %Y")
  time = now.strftime("%H:%M%p")

  print("🔍 Verifying environment variables...")
  numOfExpected =  3
  envVarsAreDefined = verify_env_vars(env_vars, numOfExpected)

  if envVarsAreDefined:
    print(f'✅ Found all {numOfExpected} environment variables.\n')
  else:
    print('❌ Failed to verify environment variables.\n')

  access_token, chat_id, bot_token = get_env_vars(env_vars)

  venmo = Venmo(access_token)
  telegram = Telegram(bot_token, chat_id)
  def dual_print(message):
    print(message)
    telegram.send_message(message)

  dual_print(f'🕘 Monthly health check running on {date} at {time}.\n')
  dual_print("🤑 Verifying Venmo client is working...")
  userId = venmo.get_user_id_by_username("Saumya-Singhal")

  if userId:
    dual_print('✅ Venmo client is working as expected.\n')
  else:
    dual_print('❌ Failed to get userId using Venmo client.\n')

  dual_print("🤑 Verifying if Venmo account has a bank payment method...")
  bank_payment_method = venmo.get_bank_payment_method()

  if bank_payment_method:
    dual_print('✅ Venmo Bank Account:')
  else:
    dual_print('❌ Failed to get payment methods using Venmo client.\n')

  returnedUserId = bool(userId)

  if envVarsAreDefined and returnedUserId:
    dual_print('✅ Everything looks good 👋 in the health check')

# Grab current date and passing in when running function
now = datetime.now()
main(now)

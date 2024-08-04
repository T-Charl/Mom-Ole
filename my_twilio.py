from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


account_sid = 'AC876374cd99fd95bce29754e00eda05a2'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Twilio in vscode',
  to='whatsapp:+27832178843'
)

print(message.sid)
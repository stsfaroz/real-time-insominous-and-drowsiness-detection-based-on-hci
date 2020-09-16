from twilio.rest import TwilioRestClient


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4a681eb1964c61bf14a5f6bea7ddadad'
auth_token = '6bd92f1b5edf42b5b039a64447d2866b'
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
                              body='Hello there!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+916381892510'
                          )

print(message.sid)
   from flask import Flask, render_template, request
   from telethon import TelegramClient
   from pyrogram import Client

   app = Flask(__name__)

   @app.route('/', methods=['GET', 'POST'])
   def index():
       session_string = None

       if request.method == 'POST':
           api_id = request.form['api_id']
           api_hash = request.form['api_hash']
           phone_number = request.form['phone_number']
           two_factor_code = request.form['two_factor_code']
           session_type = request.form['session_type']

           if session_type == 'telethon':
               client = TelegramClient('session_name', api_id, api_hash)

               async def main():
                   await client.start(phone=phone_number, password=two_factor_code if two_factor_code else None)
                   return await client.session.save()

               with client:
                   session_string = client.loop.run_until_complete(main())

           elif session_type == 'pyrogram':
               client = Client('session_name', api_id, api_hash)

               async def main():
                   await client.start(phone=phone_number, password=two_factor_code if two_factor_code else None)
                   return await client.export_session_string()

               with client:
                   session_string = client.loop.run_until_complete(main())

       return render_template('index.html', session_string=session_string)

   if __name__ == '__main__':
      app.run(debug=True)

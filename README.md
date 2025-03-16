## Kyedae Counter Bot
A discord bot version of the [kyedae counter](https://github.com/Genrevvv/kyedae_counter) GUI program.

##  Kyedae Counter Bot Commands
```
Commands                    Description
-------------------------------------------------------------------
>connect [username]         Connects to a TikTok live
>disconnect                 Disconnects to current live connection

>inc                        Manually increment counter
>inc [number]               Increment with specific amount
       
>dec                        Manually decrement counter
>dec [number]               Decrement with specific amount

>setoutchan [channelID]     Sets output channel for bye command
>setoutchan                 Set current channel as output channel

>bye                        Shutdowns the bot and 
                            outputs total count

>goodnight                  Force the bot to shutdown
```
## How to run
1. Create your Discord bot and copy its token.
2. Create a .env file in the project directory
3. Add the following line in the .env file, replace [your'bots token] with your actual bot token:
   ```
   BOT_TOKEN=[your bot's token]
5. Run the bot with the following command:
   ```
   python kyedae_counter_bot.py

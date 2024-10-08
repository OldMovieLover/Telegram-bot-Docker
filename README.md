# How to launch bot through Docker?
- You need to create an image inside Docker using the command: \
`docker build .`

- Launch the bot using the command: \
`sudo docker run -v /<PATH>/bot.log:/bot.log <IMAGE ID>` \
*IMAGE ID: You can see it using the command: `docker images`*
*PATH: Here you need to specify the full path where the bot itself is located and add /bot.log at the end, for example: `~/Downloads/latin_translator_bot/bot.log`*

- You can see all the logs in the file: \
`bot.log`

- To view running containers, also there you can copy <CONTAINER ID>, enter the command: \
`docker ps`

- To stop the bot, you need to enter the command: \
`docker stop <CONTAINER ID>`

# How does the bot work?
- To start working with the bot, write command: `/start`
- You can find out in detail how the bot works and what it uses through commands: `/help`, `/info` or by clicking the corresponding buttons.
- The main task of the bot is to perform text transliteration
- *If you write any message that the bot cannot process, it will give a reminder where will be commands or you can press any button.*

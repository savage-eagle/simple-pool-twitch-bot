# Twitch Bot Poll

Simple project to generate polls in twitch chat.

# How it works

The bot will listen to the chat and will look for the command !poll <QUESTION>.
If the command is found, the bot will create a poll with only two options to be voted: Yes and No.

The bot will also create a timer to close the poll after 10 minutes.

# Token

Please generate your token in https://twitchtokengenerator.com/ and replace the token in the file .env file.

# How to run the project in your machine

1. Clone the project
2. Install the dependencies
3. Rename `.env.sample` to `.env`
4. Add your token and channel monitoring in the `.env` file
5. Run the project with the command `python3 main.py`

# Running with Docker

1. Clone the project
2. Run the command: `docker build -t twitch_bot:latest .`
3. Rename `.env.sample` to `.env`
4. Add your token and channel monitoring in the `.env` file
5. Access the container: `docker run -it twitch_bot`

# TELEGRAM-BOT

## Local Installation

To run this project, you'll need to add the following environment variables to your `.env` file:

`TOKEN`

Clone the project

````bash
$ git clone https://github.com/Geffrerson7/iv100.git
````

Navigate to the project directory

```bash
$ cd iv100
````

Create a virtual environment

```sh
$ virtualenv venv
```

Activate the virtual environment

```
# windows
$ source venv/Scripts/activate
# Linux
$ source venv/bin/activate
```

Then install the required libraries:

```sh
(venv)$ pip install -r requirements.txt
```

Once all of that is done, proceed to start the app

```bash
(venv)$ python main.py
```

## Telegram bot's menu

Start sending coordinates:

```bash
  /iv100
```

Stop sending coordinates:
```bash
  /stop
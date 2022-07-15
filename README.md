# BorrowMon

## AlgoFi Borrow Utilization Monitor

---

Monitor your borrow utilization and set

---

&nbsp;

## Setup Environment

1. Setup Virtual Environment

```
$ python3 -m venv borrow_mon
$ cd borrow_mon
$ source bin/activate
```

> (Note: you can leave the environment by typing > deactivate())

2. Install Deps

```
$ pip install -r requirements.txt
# pip install git+https://github.com/Algofiorg/algofi-py-sdk
```

3. Create configs:

Create a file called `.env` and add the following properties...

```
TELEGRAM_API_TOKEN=<TELEGRAM BOT API TOKEN>
# Telegram Chat ID
CHAT_ID=<CHAT ID>
# Note multiple addresses supported. Separate with commas
ALGO_WALLETS=<ALGORAND PUBLIC WALLET ADDRESSES>
# Seconds between cycles. Defaults to 600 if attribute doesn't exist
SLEEP_SECONDS=<SECONDS>
```

> See here for how to create a telegram bot: https://www.techthoughts.info/how-to-create-a-telegram-bot-and-send-messages-via-api/

4. Run App

```
$ python main.py
```

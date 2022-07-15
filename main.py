from datetime import datetime
import os
import time
from dotenv import load_dotenv

import telegram
from algofi.v1.client import AlgofiMainnetClient

DEFAULT_SLEEP = 600
TIME_FMT = "%-m/%-d %-I:%M:%S %p"

class BorrowMon:
    def __init__(self):
        load_dotenv()
        sleep_sec = os.getenv('SLEEP_SECONDS')
        self.sleep_sec = int(sleep_sec) if sleep_sec is not None else DEFAULT_SLEEP
        self.chat_id = None
        self.wallets = self._get_algo_wallets()

    def run(self):
        self.bot = self.load_bot()

        while True:
            self.load_client()
            now = time.localtime()
            print(f'\n STATE - {time.strftime(TIME_FMT, now)}')
            [self.check_wallet(w, self.client) for w in self.wallets]
            time.sleep(self.sleep_sec)

    def load_client(self):
        print('Connecting to algo client...', end='', flush=True)
        w = self.wallets[0]
        self.client = AlgofiMainnetClient(user_address=w)
        print(f'CONNECTED.')

    def load_bot(self):
        telegram_api_token = os.getenv('TELEGRAM_API_TOKEN')
        if not telegram_api_token:
            raise 'Please set up TELGRAM_API_TOKEN in .env'
        self.chat_id = os.getenv('CHAT_ID')
        if not self.chat_id:
            raise 'Please set up CHAT_ID in .env'
        bot = telegram.Bot(telegram_api_token)
        print(f'Connected {bot.username} to chat: {self.chat_id}')
        return bot

    def check_wallet(self, wallet, client):
        state = client.get_user_state(wallet)

        borrowed = sum([v['borrow_usd'] for k, v in state.items() if k != 'manager'])
        borrowable = sum([v['active_collateral_max_borrow_usd'] for k, v in state.items() if k != 'manager'])
        utilization = borrowed / borrowable * 100.0

        condensed_wallet_addr = wallet[:5] + '...' + wallet[-4:]
        msg = f'Wallet: {condensed_wallet_addr} | Utilization: {round(utilization, 2)}%'
        print('\t' + msg)
        if utilization > 89.7:
            self.send_msg(msg)
            raise f'UTILIZATION EXCEEDED. {msg}'

    def send_msg(self, msg):
        self.bot.send_message(text=msg, chat_id=self.chat_id)

    def _get_algo_wallets(self):
        wallets_raw = os.getenv('ALGO_WALLETS').split(',')
        wallets = []
        for w in wallets_raw:
            wallet = w.strip()
            if wallet:
                wallets.append(wallet)
        if not wallets:
            raise 'Please set up ALGO_WALLETS in .env'
        return wallets


if __name__ == '__main__':
    app = BorrowMon()
    app.run()

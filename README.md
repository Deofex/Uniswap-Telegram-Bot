# UniSwap Telegram bot
This bot provides information when a swap or liquidity change for a specific Uniswap address occurred

## Installation
* Copy settings.default to settings.config
* Add the Telegram bot API and the etherscan API
* Change the attributes in the [PrimaryToken]  (By default these attributes are configured for the GET Protocol )
* Create a virtual environment
```
python3 -m venv env
```
* Activate the virtual environment
```
source env\bin\activate
```
* Install the depenendencies
```
pip install -r requirements.txt
```
* Join the corresponding Telegram bot a a Telegram channel and make sure it's allowed to post messages
* Active the bot by typing the command "/start" in the channel
* Start main.py and new tokens swaps and liquidity changes should appear in the channel


## Add the bot to systemd
* Create a bash file (uniswaptelegrambot.sh)
```
#!/bin/bash

HOME=/home/username
VENVDIR=$HOME/Uniswap-Telegram-Bot/env
BINDIR=$HOME/Uniswap-Telegram-Bot

cd $BINDIR
source $VENVDIR/bin/activate
python $BINDIR/main.py

```

VENVDIR is the virtual environement dir
The BINDIR is the directory where the program resides

* Create a service file (/etc/systemd/system/uniswaptelegrambot.service)

```
[Unit]
Description=Uniswap Telegram Bot
After=network.target

[Service]
Type=simple
User=username
Group=users
ExecStart=/home/username/uniswaptelegrambot.sh

[Install]
WantedBy=multi-user.target
```

* Reload, start the bot and enable it during startup
```
systemctl daemon-reload
systemctl restart uniswaptelegrambot.service
systemctl enable uniswaptelegrambot.service
```

* View the status of the bot
```
systemctl status uniswaptelegrambot.service
```
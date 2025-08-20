# tiwil-userbot
## UserBot 

A modular Telegram userbot using **telethon**.

*Repository structure:*  
userbot/ ← core bot  
  files, modules, main.py, requirements..  
private/ ← configuration and session files  
out_modules/ ← extra modules  
README.md

## Setup & Installation 

1. *Clone the Repository*
```bash
git clone https://github.com/0vernux/tiwil-userbot.git
cd tiwil-userbot
```
2. *Install dependencies*
```python
pip install -r requirements.txt
```
3. *Configure API keys*  
edit ../private/config.py and set yout API ID and API HASH:
```python
API_ID = 123456
API_HASH = "abcdef1234567890abcdef1234567890"
```
get them here:  
[Telegtam](https://my.telegram.org/apps)

## Running the bot  
```python
python main.py
```
• first run will ask for your phone number, code from Telegram and 2FA password (if enabled)  
• session files will be saved in private/ for future runs

## Modules  

The userbot comes with built-in modules located in `userbot/modules`.  
These modules are included by default.  

You can also manually download additional modules from my repository:  
👉 [0vernux/tiwil_modules](https://github.com/0vernux/tiwil_modules)  

All built-in and downloaded modules are automatically loaded at startup.  

If needed, you can manage modules using the built-in `ModuleManage` module.  
For help and a list of all available commands, use: `.help`

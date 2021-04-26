# DogeCoin-Twitter-Bot
Bot to share list of tweet using dogecoin related keywords, see [@DogeNewsBot1](https://twitter.com/DogeNewsBot1).

# Installation

Rename `.env.template` to `.env`. Access tokens will be stored in this file.

### Get your twitter credentials
#### 1/ Apply for access to [developper account](https://developer.twitter.com/en/apply-for-access)
Complete each steps, until you have access to the [Twitter Developper Portal](https://developer.twitter.com/en/portal/dashboard).
#### 2/ Create a project in the [Developper Portal](https://developer.twitter.com/en/portal/dashboard)
Store your API key and secret in `.env`.
#### 3/ Go in the settings of your application project. Edit `App permissions` to `Read and Write`.
#### 4/ Go in the `Keys and tokens` section. Generate your Access Token and and Secret.
Store this 2 extra tokens in `.env`.
  
### Install python dependencies
Require **python version >= 3.6**.  
Run `pip3 install -r requirement.txt`

# Run the bot
1/ `source .env` to load Twitter credentials in shell environnement.  
2/ `python3 main.py` will search and post list of tweets !  

Create a cron task to run the bot regulary.

# Credits

If you wan't to tips the human work behind the bot : DMZaKtgXaG1RCR2iFedW4bcbWc2q2gyhoN

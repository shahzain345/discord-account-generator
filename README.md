# Discord unclaimed account generator

Yes you heard it right, a discord unclaimed generator with a hcaptcha solver

## Requirements

An api key from: [AntiBotMail](https://antibotmail.com)

Refill on their website and add your key to the config in `Data/config.json`

Currently we only support ABM as our email provider 

## Why isn't it email verified?

Because i didnt have time to work on this shit

## Usage:

You will need two things to make this run.
Firstly you will need NodeJS: 

```bash
cd browser_hook
node app.js
```

Make sure to install all the libraries before hand by doing `npm i` inside the browser_hook folder.

Secondly you will need python
After you run the node js file, you are now ready to generate them tokens

```bash
python3 main.py
```

# Enjoy!
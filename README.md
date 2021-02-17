# Comprendebot

This is a Telegram bot that tests your ability to understand spoken language.

Intended users are constructed languages enthusiasts who rarely have an opportunity to hear their conlangs spoken.

The bot will send you voice messages and await your transcription.
If the transcription is correct, the bot will give you experience points.

Disclaimer: I'm not a software engineer, so there's probably massive antipatterns everywhere.


## Deployed instances I know

| Bot | Language | Bot's site |
| --- | -------- | ---------- |
| [@lfnescutabot](https://t.me/lfnescutabot) | [Elefen](https://www.elefen.org/) | |


## Create new instance

Let's say you want to deploy an instance for [Newspeak](https://en.wikipedia.org/wiki/Newspeak).

Do the following steps.


### Acquire Telegram token

Talk to [BotFather](https://t.me/botfather) and make a new bot. Bot's name can be anything and is not important, we really need the token.


### Download repository

Download or clone this repository to your server.


### Create language XML

Create file `language-newspeak.xml` inside `botvars/` folder.

There are examples of XML files for Elefen, Esperanto and Interslavic.

`<alphabet>` section should list letters that are worth experience points (case of letters is not important).
For Newspeak it will just contain latin.

`<transform>` section is needed if your language has several alphabets or alternative spellings for letters, and it explains how to map those alternative letters to letters in `<alphabet>`.
For Newspeak this section will be empty.


### Translate strings in Python code

Next step is to translate bot's messages from (my bad) English to Newspeak.

First, generate `.po` file:

```
pygettext3 -o newspeak.po code/
```

Open it and write translations.
See examples in `elefen.po`.

After that, convert it to `.mo` format which the bot can find and read:

```
mkdir -p locales/newspeak/LC_MESSAGES/
msgfmt -o locales/newspeak/LC_MESSAGES/cmpdbot.mo newspeak.po
```

What matters here is the resulting `cmpdbot.mo` file in a correct directory.


### Create `.env` file

Now inside `botvars/` folder create a `.env` file.
Actual name is not super important - it can be `newspeak.env`, `bot.env`, etc.
The examples below are assuming you called it just `.env`.

```
cp -n botvars/example-.env botvars/.env
chmod 0600 botvars/.env
```

Edit the variables inside it:

| Variable | Comment |
| -------- | ------- |
| `CMPDBOT_DIR` | **Type**: Path to folder<br/>**Example**: `/cmpdbot`<br/>Where all bot related stuff should be copied inside Docker container. |
| `CMPDBOT_LANGUAGE` | **Type**: Locale name<br/>**Example**: `newspeak`<br/>Language locale folder as in `locales/newspeak/LC_MESSAGES/`. |
| `CMPDBOT_LANGUAGE_SITE` | **Type**: URL<br/>**Example**: `https://en.wikipedia.org/wiki/Newspeak` |
| `CMPDBOT_LANGUAGE_FILE` | **Type**: File name<br/>**Example**: `language-newspeak.xml`<br/>Name of language XML file inside `botvars/`. |
| `CMPDBOT_SIMILARITY_RATIO` | **Type**: Float<br/>**Example**: `0.8`<br/>When one compares two phrases for similarity with Levenshtein [ratio()](https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-ratio) the result is a `float`, and if that float is greater than the value of `CMPDBOT_SIMILARITY_RATIO`, the two phrases are considered "similar". Right now, the bot doesn't do much about it, but in the future versions it might use this value for better phrases management. |
| `CMPDBOT_TOKEN` | **Type**: Telegram API token<br/>**Example**: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`<br/>The secret that you've acquired from [BotFather](https://t.me/botfather). |
| `CMPDBOT_LOCALE_DIR` | **Type**: Path to folder<br/>**Example**: `/cmpdbot/locales`<br/>Where bot will find its localization inside container. |
| `CMPDBOT_LINK` | **Type**: URL<br/>**Example**: `https://newspeak.bot/`<br/>Official site of your bot if there is one. |
| `CMPDBOT_L10N_DOMAIN` | **Type**: Lacale domain<br/>**Example**: `cmpdbot`<br/>File name of `locales/newspeak/LC_MESSAGES/cmpdbot.mo` without `.mo` suffix. |
| `CMPDBOT_EXCHANGE_DIR_LOCAL` | **Type**: Path to folder<br/>**Example**: `/home/wsmith/newspeak-bot-volume`<br/>Folder that will serve as a Docker volume on **client machine**. |
| `CMPDBOT_EXCHANGE_DIR_CONTAINER` | **Type**: Path to folder<br/>**Example**: `/cmpdbot/exchange`<br/>Folder that will serve as a Docker volume inside **container**. |
| `CMPDBOT_CONST_START` | **Type**: String<br/>**Example**: `start`<br/>Callback data of a start button. (Technical value. Leave as is.) |
| `CMPDBOT_MIN_SILVER` | **Type**: Float<br/>**Example**: `0.7`<br/>If the transcription's similarity to the original phrase is higher than this value, send user "silver medal" sticker. |
| `CMPDBOT_MIN_BRONZE` | **Type**: Float<br/>**Example**: `0.3`<br/>If the transcription's similarity to the original phrase is higher than this value, send user "bronze medal" sticker. |
| `CHOOSE_SEVRAL_TIMEZ` | **Type**: Integer<br/>**Example**: `5`<br/>Max amount of consecuitive challange lookups. (Technical value. Leave as is.) |
| `CHOOSE_CHANCE_PHRASE` | **Type**: Integer<br/>**Example**: `1`<br/>How often should user be asked to add a new phrase to database. The greater the more often. |
| `CHOOSE_CHANCE_VOICE` | **Type**: Integer<br/>**Example**: `3`<br/>How often should user be asked to submit a voice message. The greater the more often. |
| `CHOOSE_CHANCE_TRANSCRIPTION` | **Type**: Integer<br/>**Example**: `9`<br/>How often should user be asked to transcribe a voice message. The greater the more often. |
| `CHOOSE_MIN_XP_PHRASE` | **Type**: Integer<br/>**Example**: `1000`<br/>How many experience points should user have before they're allowed to add a new phrase to database. |
| `CHOOSE_MIN_XP_VOICE` | **Type**: Integer<br/>**Example**: `100`<br/>How many experience points should user have before they're allowed to submit a voice message. |
| `CHOOSE_SAMPLE_PHRASE` | **Type**: Integer<br/>**Example**: `10`<br/>How many random phrases should be selected from database before inputting them to the chooser module. Making it less will increase "randomness". |
| `CHOOSE_SAMPLE_VOICE` | **Type**: Integer<br/>**Example**: `10`<br/>How many random voice recordings should be selected from database before inputting them to the chooser module. Making it less will increase "randomness". |
| `CHOOSE_SUCCESS_BOOST` | **Type**: Integer<br/>**Example**: `7`<br/>The amount of letters the user transcribes correctly is saved as their "last success". Next time the bot will try to choose a phrase with length closer to last success + boost. |
| `CHOOSE_HOLD_SECONDS` | **Type**: Integer<br/>**Example**: `172800`<br/>Amount of seconds that should pass before user's phrase or voice recording can be used as a challenge to other users. |
| `LOG_LEVEL` | **Type**: String<br/>**Example**: `DEBUG` |
| `POSTGRES_USER` | **Type**: String<br/>**Example**: `newspeakbot` |
| `POSTGRES_PASSWORD` | **Type**: String<br/>**Example**: `newspeakbot2+2=5` |
| `POSTGRES_HOST` | **Type**: String<br/>**Example**: `pg`<br/>Postgres host name. If you plan to use supplied Compose file and hence its Postgres container, keep value `pg`. |
| `POSTGRES_PORT` | **Type**: Integer<br/>**Example**: `5432` |
| `POSTGRES_DB` | **Type**: String<br/>**Example**: `newspeakbot` |
| `MIGRATIONS_SYNC` | **Type**: Boolean<br/>**Example**: `1`, nothing<br/>Whether or not the bot should delay its start until database migrations apply. It generally should. (Why did I make it configurable?) |
| `MIGRATIONS_HOST` | **Type**: String<br/>**Example**: `migrations`<br/>Host name of the container that runs database migrations. If you plan to use supplied Compose file, keep value `migrations`. |
| `MIGRATIONS_PORT` | **Type**: Integer<br/>**Example**: `10946` |
| `S3_HOST` | **Type**: String<br/>**Example**: `s3`<br/>S3 host name. If you plan to use supplied Compose file and hence its Minio container, keep value `s3`. |
| `S3_PORT` | **Type**: Integer<br/>**Example**: `9000` |
| `S3_ACCESS_KEY` | **Type**: String<br/>**Example**: `newspeakbot` |
| `S3_SECRET_KEY` | **Type**: String<br/>**Example**: `newspeakbot2+2=1984` |
| `S3_VOICES_BUCKET` | **Type**: String<br/>**Example**: `newspeakbotvoices`<br/>Name of the S3 bucket where the voice binaries should be stored. |
| `STICKER_PHR` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMDYCujE1oR-Zjt5IwdddnxkWQxPCIAAhMAA2XuFBAo2PGrWKbT_B4E`<br/>Phrase challenge sticker. |
| `STICKER_VOC` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMEYCujRVhYHR18bF0j60fLGjuwLqAAAhIAA2XuFBD_h-TjUQABNUMeBA`<br/>Voice recording challenge sticker. |
| `STICKER_TRS` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMFYCuja-pqNrFBdkDsM9WayDeI1twAAhEAA2XuFBBBkQ7Dv-7Ufh4E`<br/>Transcription challenge sticker. |
| `STICKER_GOLD` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMGYCujn4-bfI6aGs6695L5Yc5fn3wAAhcAA2XuFBB3ge6WMuz0fx4E`<br/>Gold medal sticker. |
| `STICKER_SILVER` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMHYCujxdhBazEQ4PPC2onSHXBPNnQAAhgAA2XuFBApYLlTBEVLlR4E`<br/>Silver medal sticker. |
| `STICKER_BRONZE` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMIYCukAocAAXoPOcKVRUR7NC8Pe2u7AAIZAANl7hQQFV0zhLMubpkeBA`<br/>Bronze medal sticker. |
| `STICKER_PAPER` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMJYCukLP7LfgTJsgWP-5UdwFs4_zIAAhoAA2XuFBD0kfJTn_og1x4E`<br/>Toilet paper medal sticker. |
| `STICKER_OK_PHR` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMKYCukXpn-u1JeJ8hPGkKOs8EvnlgAAhUAA2XuFBAhgOshJBjTZx4E`<br/>Phrase saved sticker. |
| `STICKER_OK_VOC` | **Type**: String<br/>**Example**: `CAACAgIAAxkBAAMLYCukhUOv1jZb-qPiTxBrh0dMWdkAAhYAA2XuFBCSPYJGjfEo4R4E`<br/>Voice saved sticker. |


### Launch

There are probably better, more efficient ways to do this. Anyway...

Create environment variable `DOTENV_FILE` holding your .env file name - just `.env` here in the examples.

```
export DOTENV_FILE=.env
```

Now invoke `docker-compose up`:

```
docker-compose --env-file botvars/$DOTENV_FILE up --scale manage=0 --build --remove-orphans
```

It will produce a lot of output while downloading and starting everything.

You know that it (probably) worked when you see `INFO:aiogram.dispatcher.dispatcher:Start polling.`.
Now stop it with `Ctrl+C` and relaunch everything in a background with `-d`.

```
docker-compose --env-file botvars/$DOTENV_FILE up --scale manage=0 --build --remove-orphans -d
```


### Add phrases

Next step is adding some initial Newspeak phrases to the bot's database.

Inside `manage` container there's a command for it: `botaddphrases`.
It takes a file where each line contains one phrase and adds them all in one go.

Create file `phrases.txt` inside the Docker volume folder (`CMPDBOT_EXCHANGE_DIR_LOCAL`):

```
cat > phrases.txt <<1984
War is peace.
Freedom is slavery.
Ignorance is strength.
1984
```

Now launch the `manage` container:

```
docker-compose --env-file botvars/$DOTENV_FILE run --rm manage bash
```

And inside the container invoke the command:

```
botaddphrases $CMPDBOT_EXCHANGE_DIR_CONTAINER/phrases.txt
```

Sometimes the command will complain about similar phrases that are already in the database.
Type `y` if you wish to insert the phrase nonetheless.


### Add voice recordings

Almost there.
Now it's time to add voice recordings.

It's easy to do through the bot itself.
Start conversation with it in Telegram and it will send you voice recording tasks.

Pay attention though that if you've set `CHOOSE_MIN_XP_VOICE` to anything greater than `0`, the bot will send you nothing because your XP is `0`.

To bypass it you can cheat your XP in database:

```
docker exec -ti $( docker ps -f "ancestor=postgres" -q ) bash
psql -U $POSTGRES_USER
UPDATE person SET xp = 9000 WHERE id = <YOUR ID>;
```

Or you can temporarily set `CHOOSE_MIN_XP_VOICE` to `0` and restart the bot:

```
docker-compose restart
```


### One last step (optional)

Let me know about your instance so I could update my table of existing bots. Thank you.


## Roadmap

Things that also should be added soon

- Easy monitoring
- Admin site
- In-bot reporting
- Show best XP
- Async Sqlalchemy

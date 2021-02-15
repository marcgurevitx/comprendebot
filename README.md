# Comprendebot

`comprendebot` is a Telegram bot for testing one's ability to understand spoken language.

It's intended users are constructed language enthusiasts who don't always have an easy way to hear their conlangs spoken.

This bot sends users voice messages and awaits the transcriptions.
If a transcription is correct, the user is given experience points.


## Instances known to me

| Bot | Language | Bot's site |
| --- | -------- | ---------- |
| https://t.me/lfnescutabot | [Lingua Franca Nova](https://www.elefen.org/) | |


## Create new instance

For illustration we will create an instance of `comprendebot` for **Newspeak** (2+2=5).

Disclaimer: I'm not a computer engineer.
Be ready to encounter suboptimal antipatterns.


### Acquire Telegram token

Talk to [BotFather](https://t.me/botfather) and make a new bot.


### Download repository

Download/clone this repository to your server.


### Create language XML

Create file `language-newspeak.xml` inside `botvars/` folder.

Use existing XMLs for Elefen, Esperanto and Interslavic as examples.

`<alphabet>` section should list letters that are worth experience points (case of letters is not important).
For Newspeak it will just contain latin.
`<transform>` section is needed if your language has several alphabets or alternative spellings for letters.
It should explain how to map those alternative letters to letters in `<alphabet>`.
For Newspeak this will be empty.


### Translate strings in Python code

```
pygettext3 -o newspeak.po code/
# Translate strings in newspeak.po
mkdir -p locales/newspeak/LC_MESSAGES/
msgfmt -o locales/newspeak/LC_MESSAGES/cmpdbot.mo newspeak.po
```

What matters here is the resulting `cmpdbot.mo` in a correct directory.

See `elefen.po` for how localization is done.


### Create `.env` file

Now inside `botvars/` folder create another file: `.env`:

```
cp -n botvars/example-.env botvars/.env
```

Edit the variables inside `.env`:

| Variable | Type | Example | Meaning |
| -------- | ---- | ------- | ------- |
| `CMPDBOT_DIR` | Path to folder | `/cmpdbot` | Where all bot related stuff should be copied inside Docker container. |
| `CMPDBOT_LANGUAGE` | Locale name | `newspeak` | Language locale folder as in `locales/newspeak/LC_MESSAGES/`. |
| `CMPDBOT_LANGUAGE_SITE` | URL | `https://en.wikipedia.org/wiki/Newspeak` | |
| `CMPDBOT_LANGUAGE_FILE` | File name | `language-newspeak.xml` | Language XML file inside `botvars/`. |
| `CMPDBOT_SIMILARITY_RATIO` | Float | `0.8` |
    When one compares two phrases for similarity with [ratio()](https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-ratio) the result is a `float`.
    If it's greater than `CMPDBOT_SIMILARITY_RATIO`, the two phrases are considered similar.
    Right now, the bot doesn't do much about it, but in future versions it might use this value to manage and lookup phrases.
    |
| `CMPDBOT_TOKEN` | Telegram API token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` | The secret that we've acquired from [BotFather](https://t.me/botfather). |
| `CMPDBOT_LOCALE_DIR` | Path to folder | `/cmpdbot/locales` | Where bot will find its localization. |
| `CMPDBOT_LINK` | URL | `https://newspeak.bot/` | Official site of your bot if there is one. |
| `CMPDBOT_L10N_DOMAIN` | Lacale domain | `cmpdbot` | File name of `locales/newspeak/LC_MESSAGES/cmpdbot.mo` without `.mo`. |
| `CMPDBOT_EXCHANGE_DIR_LOCAL` | Path to folder | `/home/wsmith/newspeak-bot-volume` | Folder that will serve as a Docker volume on **client machine**. |
| `CMPDBOT_EXCHANGE_DIR_CONTAINER` | Path to folder | `/cmpdbot/exchange` | Folder that will serve as a Docker volume inside **container**. |
| `CMPDBOT_CONST_START` | String | `start` | Callback data of a start button. (Technical value. Leave as is.) |
| `CMPDBOT_MIN_SILVER` | Float | `0.7` | If transcription similarity ratio is higher than this, send user "silver medal" sticker. |
| `CMPDBOT_MIN_BRONZE` | Float | `0.3` | If transcription similarity ratio is higher than this, send user "bronze medal" sticker. |
| `CHOOSE_SEVRAL_TIMEZ` | Integer | `5` | Max amount of consecuitive challange lookups. (Technical value. Leave as is.) |
| `CHOOSE_CHANCE_PHRASE` | Integer | `1` | How often should user be asked to add a new phrase to database. The greater the more often. |
| `CHOOSE_CHANCE_VOICE` | Integer | `3` | How often should user be asked to submit a voice message. The greater the more often. |
| `CHOOSE_CHANCE_TRANSCRIPTION` | Integer | `9` | How often should user be asked to transcribe a voice message. The greater the more often. |
| `CHOOSE_MIN_XP_PHRASE` | Integer | `1000` | How many experience points should user have before they're allowed to add a new phrase to database. |
| `CHOOSE_MIN_XP_VOICE` | Integer | `100` | How many experience points should user have before they're allowed to submit a voice message. |
| `CHOOSE_SAMPLE_PHRASE` | Integer | `10` |
    How many random phrases should be selected from database before inputting them to the chooser module.
    Making it less will increase "randomness".
    |
| `CHOOSE_SAMPLE_VOICE` | Integer | `10` |
    How many random voice recordings should be selected from database before inputting them to the chooser module.
    Making it less will increase "randomness".
    |
| `CHOOSE_SUCCESS_BOOST` | Integer | `7` |
    The amount of letters the user transcribes correctly is saved as their "last success".
    Next time the bot will try to choose a phrase that is closer to length = last success + boost.
    |
| `CHOOSE_HOLD_SECONDS` | Integer | `172800` | Amount of seconds that should pass before user's phrase or voice recording can be sent as a challenge to other users. |
| `LOG_LEVEL` | String | `DEBUG` | |
| `POSTGRES_USER` | String | `newspeakbot` | |
| `POSTGRES_PASSWORD` | String | `newspeakbot2+2=5` | |
| `POSTGRES_HOST` | String | `pg` |
    Postgres host name.
    If you plan to use supplied Compose file and hence its Postgres container, keep value `pg`.
    |
| `POSTGRES_PORT` | Integer | `5432` | |
| `POSTGRES_DB` | String | `newspeakbot` | |
| `MIGRATIONS_SYNC` | Boolean | nothing or `1` |
    Whether or not the bot should delay its start until database migrations apply.
    It generally should.
    (Why did I make it configurable?)
    |
| `MIGRATIONS_HOST` | String | `migrations` |
    Host name of the container that runs database migrations.
    If you plan to use supplied Compose file, keep value `migrations`.
    |
| `MIGRATIONS_PORT` | Integer | `10946` | |
| `S3_HOST` | String | `s3` |
    S3 host name.
    If you plan to use supplied Compose file and hence its Minio container, keep value `s3`.
    |
| `S3_PORT` | Integer | `9000` | |
| `S3_ACCESS_KEY` | String | `newspeakbot` | |
| `S3_SECRET_KEY` | String | `newspeakbot2+2=1984` | |
| `S3_VOICES_BUCKET` | String | `newspeakbotvoices` | Name of the S3 bucket where the voice binaries should be kept. |
| `STICKER_PHR` | String | `CAACAgIAAxkBAAICxWAm3KnYUP2AmEKmjt5MBIhvuLe5AAITAANl7hQQKNjxq1im0_weBA` | Phrase challenge sticker. |
| `STICKER_VOC` | String | `CAACAgIAAxkBAAIC4WAm4NxwgRTQ5OHso5Or_r0DKzcSAAISAANl7hQQ_4fk41EAATVDHgQ` | Voice recording challenge sticker. |
| `STICKER_TRS` | String | `CAACAgIAAxkBAAIC4mAm4VT3gBqzXUL23UeQ5S0u_m28AAIRAANl7hQQQZEOw7_u1H4eBA` | Transcription challenge sticker. |
| `STICKER_GOLD` | String | `CAACAgIAAxkBAAIC42Am4XkAAVXct6g8RnoU__SGaUHErQACEAADZe4UEJZVJfMWjQABAh4E` | Gold medal sticker. |
| `STICKER_SILVER` | String | `CAACAgIAAxkBAAIC5GAm4ahzqZMgrgL5hPMJ-FeNqoZEAAIPAANl7hQQ9HlkTNOaa0keBA` | Silver medal sticker. |
| `STICKER_BRONZE` | String | `CAACAgIAAxkBAAIC5WAm4bseD86pXShQMhq3fiwBdAE1AAIOAANl7hQQ1yWkknXfGbEeBA` | Bronze medal sticker. |
| `STICKER_PAPER` | String | `CAACAgIAAxkBAAIEBmApHZVRREqnPntKA3Pe54BZm8-uAAIUAANl7hQQlRYCZ1WIrj4eBA` | Toilet paper medal sticker. |


### Launch

```
export DOTENV_FILE=.env
docker-compose --env-file botvars/$DOTENV_FILE up --scale manage=0 --build --remove-orphans
```

It will produce a lot of output while downloading and starting everything.

Seeing `ERROR`s and `Traceback`s is probably a bad sign - pressing `Ctrl+C` and start debugging.

You know that it probably worked when you see `INFO:aiogram.dispatcher.dispatcher:Start polling.`.
Now stop it (`Ctrl+C`) and relaunch everything in a background with `-d`.

```
docker-compose --env-file botvars/$DOTENV_FILE up --scale manage=0 --build --remove-orphans -d
```


### Add phrases

Bot's database is empty so we should add phrases.
Inside the volume folder (`CMPDBOT_EXCHANGE_DIR_LOCAL`) create a simple text file, e.g `phrases.txt`, where each line contains one phrase.

Now launch `manage` container and execute `botaddphrases` command:

```
docker-compose --env-file botvars/$DOTENV_FILE run --rm manage bash
botaddphrases $CMPDBOT_EXCHANGE_DIR_CONTAINER/phrases.txt
```

This command may complain about a similar phrase already in database.
Input `y` if you wish to add the phrase nonetheless.


### Add voice recordings

You can add voice recordings throu the bot itself.
Start conversation with it in Telegram and it will send you such challenges.

Pay attention though that if you've set `CHOOSE_MIN_XP_VOICE` to anything greater than `0`, bot will send you nothing because your XP is `0`.

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

## Roadmap

In future versions I'm planning to add admin site and in-bot reporting.

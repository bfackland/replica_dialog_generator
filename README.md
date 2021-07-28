# replica_dialog_generator

**Auto-generate dialog audio files using the Replica Studios 'AI Voices' API.**

## What does this do? Why would you want to use it?

You want to generate audio files for the text dialog you are using in your
creative chatbot project, so that your code can 'speak', in a 'realistic',
perhaps even unique voice, to the end-user.

You can use this utility standalone, or within a Rasa project folder.

### What is Replica Studios?

To quote [their website](https://replicastudios.com):

> AI voice actors for games + films

> It all starts with a talented voice actor spending hours training our AI how
> to perform.
> Our AI model learns how to perform by copying the real voice actors unique
> speech patterns, pronunciation, and emotional range.
> The end result is an AI voice actor you can use in your games or films.

### What is Rasa?

To quote [their website](https://rasa.com):

> Rasa is the leading conversational AI platform, for personalized
> conversations at scale.

> Rasa Open Source is a framework for natural language understanding,
> dialogue management, and integrations. Rasa X is a free toolset used to
> improve virtual assistants built using Rasa Open Source. Together, they
> include all the features to create powerful text- and voice-based assistants
> and chatbots.

## Licence

This utility is distributed under GNU General Public License v3.0,
which can be found in the file LICENCE.txt. In summary:

> Permissions of this strong copyleft license are conditioned on making
> available complete source code of licensed works and modifications,
> which include larger works using a licensed work, under the same license.
> Copyright and license notices must be preserved.
> Contributors provide an express grant of patent rights.

## Setup Replica Studios API

First you'll need an account with Replica Studios. As of July 2021 you get
30 minutes of free credit when you sign up. If you use the following referral
link, you get 60 minutes:

https://replicastudios.com/account/signup?referral_code=Xe07Evdx

Once you have an active account, put your credentials in a local file so that
the dialog generation script can authenticate you against the API:

```
# replica_api_credentials.json
{
  "client_id" : "<your replica username>",
  "secret" : "<your replica password>"
}
```

(Note: `replica_api_credentials.json` should not be added or pushed to a
Git repo and is ignored in `.gitignore` by default.)

Next you'll need to specify the name and Replica UID of a voice to generate
audio files with. Here's an example:

```
# replica_config.json
{
  "replica_voice_uids" : {
    "amber" : "4807ea95-5b17-43b7-b25d-e409736a099f",
    "thomas" : "c7c81053-7ac3-4b2f-9809-0be6fae07ca5"
  }
}
```

At the time of writing (July 2021) it only seems possible to obtain the UID
by viewing the source of the Replica website Project page when selecting
a voice.

## Prepare Your Dialog

You'll need a `dialog` folder and a `responses.yml` file in your current/project
folder, defining the dialog to be generated:

```
mkdir dialog
```

Here's a simple example `responses.yml` taken from the
[Rasa v2 documentation](https://rasa.com/docs/rasa/responses/):

```
# ./dialog/responses.yml
---
version: "2.0"

responses:
  utter_greet:
  - text: "Hi there!"
  utter_bye:
  - text: "See you!"
```

## Configure Python Environment

Now create a Python
[virtual environment](https://docs.python.org/3/library/venv.html) (venv) and
install the package dependencies defined in `requirements.txt`:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Generate Audio using an AI Voice

If you've made it this far you should now be able to run `generate_dialog.py`
which will work through all the dialog in `./dialog/responses.yml` and attempt
to generate OGG audio files for each (using the *first* voice you specify in
  `replica_config.json`):

```
python generate_dialog.py
```

## Troubleshooting

Problem: `ModuleNotFoundError`, e.g. for 'requests':

```
% python generate_dialog.py
Traceback (most recent call last):
  File "generate_dialog.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

Solution: Make sure you've installed the depdendencies using pip3 (as above),
then (re-)activated your venv prior to running:

```
source ./venv/bin/activate
python generate_dialog.py
```

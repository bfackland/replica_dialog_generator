# replica-dialog-generator

Generate dialog using the Replica Studios 'AI Voices' API
---------------------------------------------------------

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

Important: `replica_api_credentials.json` should not be added or pushed to a
Git repo and is ignored in `.gitignore` by default.

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

If you've made it this far you should now be able to run `generate_dialog.py`
which will work through all the dialog in `../dialog/responses.yml` and attempt
to generate OGG audio files for each (using the first voice you specify in
  `replica_config.json`):

```
python generate_dialog.py
```

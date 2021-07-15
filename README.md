# replica-dialog-generator

Generating Dialog using Replica API
-----------------------------------

First you'll need some local Replica API credentials:

```
# replica_api_credentials.json
{
  "client_id" : "<your replica username>",
  "secret" : "<your replica password>"
}
```

Then run `generate_dialog.py` to work through all the dialog in `responses.yml` and
attempt to generate OGG audio files for each:

```
python generate_dialog.py
```

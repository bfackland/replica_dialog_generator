import requests
import sys
from loguru import logger
from dialog import Dialog, DIALOG_PATH
import json


REPLICA_API_CREDENTIALS_FILENAME = "./replica_api_credentials.json"


def make_api_request(url, request_type='get', data={}, params={}, headers={}):
    """
    GET and POST requests send data in different formats
    use this common method for both, which also handles HTTP response codes
    """
    if request_type == 'get':
        api_response = requests.get(url, params=params, headers=headers)
    elif request_type == 'post':
        api_response = requests.post(url, data=data, headers=headers)

    if api_response.status_code not in [200, 202]:
        logger.error("Received unknown response code from API; aborting.")
        sys.exit()

    try:
        api_response_json = api_response.json()
    except:
        logger.error("Couldn't get JSON from API response; aborting.")
        sys.exit()

    return api_response.status_code, api_response_json

def get_access_token():
    """
    in order to use the Replica API we must first have an access token
    which is generated by authenticating with our Replica credentials

    more info: https://docs.replicastudios.com/?python#replica-api-api-endpoints

    we load our personal Replica credentials from a local json file
    """
    logger.info(f"Using Replica API credentials from {REPLICA_API_CREDENTIALS_FILENAME}")
    with open(REPLICA_API_CREDENTIALS_FILENAME, 'r') as rapifile:
        replica_api_credentials = json.loads(rapifile.read())

    _, api_response_json = make_api_request(
        "https://api.replicastudios.com/auth", request_type='post',
        data=replica_api_credentials,
        )

    try:
        access_token = api_response_json['access_token']
    except:
        logger.error("Couldn't get an access_token from remote API; aborting.")
        sys.exit()

    return access_token

def get_speech(access_token, text_key, text, voice_uid):
    """
    using a Replica API access token that we have already obtained, make a
    request to the API to generate one line of dialog
    if that's successful, we get back a download URL where we then fetch the
    speech file from, returning the binary data
    """
    # TODO: could be looked up automatically by 'make_api_request'
    # e.g. stored on a class
    headers = {
        'Authorization': f'Bearer {access_token}'
        }

    params={
        'txt' : text,  'speaker_id' : voice_uid,
        'extension' : 'ogg', 'bit_rate' : '128', 'sample_rate' : '44100',
        }

    api_response_status_code, api_response_json = make_api_request(
    "https://api.replicastudios.com/speech", request_type='get',
    params=params, headers=headers
    )

    if api_response_status_code == 202:
        # fetch speech file already generated
        pass
    else:
        # store newly generated speech file to disk
        download_url = api_response_json['url']
        logger.info(f"Downloading generated audio from {download_url}...")
        download_response = requests.get(download_url)
        return download_response.content

    return None

def generate_dialog():
    access_token = get_access_token()
    dialog = Dialog()
    voice, voice_uid = list(dialog.replica_voice_uids.items())[0]
    responses = dialog.load_responses()
    count = 0

    for text_key, text in responses.items():
        if text_key.startswith("PA_"): continue
        dialog_file = dialog.get_dialog_file_for_text(text)
        if not dialog_file:
            logger.info(f"""Generating dialog for text "{text}"...""")
            speech_data = get_speech(access_token, text_key, text, voice_uid)
            if speech_data:
                text_md5 = dialog.get_text_md5(text)
                dialog_filename = f"{voice}_{text_key}_{text_md5}.ogg"
                with open(f"{DIALOG_PATH}/{dialog_filename}", 'wb') as f:
                    f.write(speech_data)
                    logger.info(f"Wrote {dialog_filename} to disk")
                    count += 1

    if count > 0:
        logger.info(f"Generated {count} dialog files; total = {len(responses)}")
    else:
        logger.info("Didn't need to generate any new dialog files.")

if __name__ == "__main__":
    generate_dialog()

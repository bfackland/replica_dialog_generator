from loguru import logger
import yaml
import hashlib
from os import listdir
import json
from os.path import exists


DIALOG_PATH = "./dialog/"
DIALOG_FILES = [ x for x in listdir(DIALOG_PATH) if x.lower().endswith('.ogg')]
REPLICA_CONFIG_FILENAME = "./replica_config.json"
if not exists(REPLICA_CONFIG_FILENAME):
    REPLICA_CONFIG_FILENAME = "./replica_dialog_generator/replica_config.json"


class Dialog:
    def __init__(self):
        replica_config = self.load_replica_config()
        self.replica_voice_uids = replica_config['replica_voice_uids']

    def load_replica_config(self):
        """
        load the project-specific Replica configuration from a json file
        """
        logger.info(f"Using Replica Config from {REPLICA_CONFIG_FILENAME}")
        with open(REPLICA_CONFIG_FILENAME, 'r') as rcfile:
            replica_config = json.loads(rcfile.read())
        return replica_config

    def normalise_text(self, text):
        """
        converts multi-line text with multiple spaces into one string that
        is more consistent
        """
        text = text.strip()
        text = text.replace('\n', ' ')
        while '  ' in text:
            text = text.replace('  ', ' ')
        return text

    def load_responses(self):
        """
        loads the dialog responses data structure from yaml and returns
        in a lookup-table format (text_key, text)
        """
        responses = {}
        logger.info("Reading responses from disk...")
        with open(f'{DIALOG_PATH}responses.yml', 'r') as file:
            data = yaml.safe_load(file)
            if 'responses' in data.keys():
                for k, v in data['responses'].items():
                    responses[k] = self.normalise_text(v[0]['text'])
        logger.info(f"Loaded {len(responses)} responses.")
        return responses

    def get_text_md5(self, text):
        """
        compute the md5 hash of a (normalised) text string
        """
        text = self.normalise_text(text)
        text_md5 = hashlib.md5(text.encode('ascii')).hexdigest()
        return text_md5

    def get_dialog_file_for_text(self, text):
        """
        look to see if we have a dialog file that matches the hash of the
        text that we want to say
        """
        text_md5 = self.get_text_md5(text)
        dialog_file = [ x for x in DIALOG_FILES if text_md5 in x ]

        if dialog_file:
            if len(dialog_file) == 1:
                dialog_file = dialog_file[0]
            elif len(dialog_file) > 1:
                logger.warning(f"""Multiple dialog files found for text "{text}" (hash {text_md5})""")
        else:
            logger.info(f"""No dialog file found for hash {text_md5}""")

        return dialog_file

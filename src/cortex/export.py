import os
from cortex.record import Record
from dotenv import load_dotenv
from datetime import datetime
from config import *

#
record_name = datetime.now().strftime('%H.%M.%S_%d-%m-%y')

# folder
record_export_folder = os.getcwd() + '/records'
if not os.path.exists(record_export_folder):
    os.makedirs(record_export_folder, exist_ok=True)


# Load ENV
dotenv_path = './.env'
load_dotenv(dotenv_path)
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
assert client_id is not None and client_secret is not None, \
    "Failed to load <.env> file"
print(f">>>.Env Loaded, Client ID: {client_id}")


# RECORD
r = Record(client_id, client_secret)
r.record_title = record_name # required param and can not be empty
r.record_description = '' # optional param

r.record_export_folder = record_export_folder
r.record_export_data_types = ['EEG']
r.record_export_format = 'CSV'
# r.record_export_format = 'EDF'
r.record_export_version = 'V2'


def start_recording_experiment(**kwargs):
    """
    
    """
    print(f"\n>>>[record_eeg_thread] --> start_recording_experiment()")

    record_duration_s = kwargs["n_trials"] * \
                        (DURATION_OF_TRIAL + DELAY_BETWEEN_TRIALS)
    # real record duration
    r.start(record_duration_s)




def stop_recording_experiment():
    r.stop_record()

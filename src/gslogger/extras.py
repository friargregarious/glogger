from pathlib import Path
import json
import datetime


def date(reporting=None) -> str:
    """
    Returns the current date and time as a string
    format: "YYYY-MM-DD-HH-MM-SS" for filenames
            "YYYY-MM-DD"          for reporting.

    :return: A string representing the current date and time
    """
    if reporting is not None:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")




def save_json(data, target) -> None:
    """
    Saves the configuration to a file named "glog.json".

    :param data: The configuration data to be saved
    :param target: The file path to save the configuration to
    :return: None
    """
    try:
        with open(target, "w") as fs:
            fs.write(json.dumps(data, indent=4, sort_keys=True))

        print(f"SAVE_JSON: {target} saved successfully.")

    except Exception as e:
        raise Exception(f"SAVE_JSON: Error saving {target}: {e}")
        # print(f"SAVE_JSON: Error saving {target}: {e}")


def load_json(src) -> dict:
    """
    Loads the configuration from the src file.

    :return: The configuration data
    """
    try:
        with open(src, "r", encoding="utf-8") as fs:
            config_data = json.loads(fs.read())
            print(f"LOAD_JSON: successfully loaded {src}")
            return dict(config_data)

    except Exception as e:
        raise Exception(f"LOAD_JSON: Error loading {src}: {e}")
        # print(f"LOAD_JSON: Error loading {src}: {e}")

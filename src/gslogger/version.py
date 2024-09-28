import pathlib

try:
    from extras import load_json
except:
    from .extras import load_json
    

# with open("glog.json", "r", encoding="utf-8") as fs:
#     config_data = load_json(fs.read())
config_loc = pathlib.Path(__file__).parent
config_data = load_json(config_loc / "glog.json")

__version__ = "v" + ".".join(map(str, config_data["app"]["version_number"]))

__author__ = config_data["dev"]["developer"]

__author_email__ = config_data["dev"]["dev_email"]

import toml

with open("glog.toml", "r", encoding="utf-8") as toml_file:
    config_data = toml.loads(toml_file.read())

# __version__ = "0.2.58"
__version__ = ".".join([str(x) for x in config_data["app"]["version_number"]])

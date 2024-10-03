from pathlib import Path

try:
    from extras import load_json
except:
    from .extras import load_json


# with open("glog.json", "r", encoding="utf-8") as fs:
#     config_data = load_json(fs.read())

# def find_path(filename:str):
#     """
#     Recursively searches for the specified file, starting from the given path.

#     :param filename: The name of the file to search for.
#     :param path: The path to start searching from. Defaults to the current working directory.
#     :return: A Path object representing the location of the file.
#     """
#     path = Path(__file__).parent
#     while True:
#         if (path / filename).exists():
#             return path / filename

#         path = path.parent
        
#         if path.parts == ():
#             return Exception(f"File not found: {filename}")
        
try:
    # config_data = load_json(find_path("glog.json"))
    config_data = load_json(Path.cwd() / "glog.json")

    __version__ = "v" + ".".join(map(str, config_data["app"]["version_number"]))
    __author__ = config_data["dev"]["developer"]
    __author_email__ = config_data["dev"]["dev_email"]

except Exception as e:
    __version__ = "v0.0.0"
    __author__ = "No Author"
    __author_email__ = "No Email"

    # raise Exception(f"VERSION: Error loading glog.json: {e}")
    # print(f"LOAD_JSON: Error loading glog.json: {e}")


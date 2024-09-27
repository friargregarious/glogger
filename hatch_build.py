import json
import os
from hatchling.metadata.plugin.interface import MetadataHookInterface

class JSONMetaDataHook(MetadataHookInterface):
    def update(self, metadata):
        src_file = os.path.join(self.root, "gnumeric", ".constants.json")
        with open(src_file) as src:
            constants = json.load(src)
            metadata["version"] = constants["__version__"]
            metadata["license"] = constants["__license__"]
            metadata["authors"] = [
                {"name": constants["__author__"], "email": constants["__author_email__"]},
            ]

import json

class Config:
    PARAM = None
    def loadconfig(self, path):
        with  open(path, 'r') as f:
            self.PARAM = json.load(f)



class CaseInsensitiveDict(dict):
    def __init__(self, *args, **kwargs):
        orig = dict(*args, **kwargs)
        new = {key.lower(): value for key, value in orig.items()}
        super().__init__(new)

    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

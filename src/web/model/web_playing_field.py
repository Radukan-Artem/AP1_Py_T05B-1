class WebPlayingField:
    def __init__(self, new_field = None):
        if new_field is None:
            self.field = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        else:
            self.field = new_field
        
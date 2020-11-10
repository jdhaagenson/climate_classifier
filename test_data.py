class LocationData:
    """
    convenient helper for working with test data
    """
    def __init__(self, name, prec_list, temp_list, north=True, elevation=0):
        self.name = name
        self.prec = prec_list
        self.temp = temp_list
        if north:
            self.hem = 'N'
        else:
            self.hem = 'S'
        self.elev = elevation



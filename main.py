

def feet_to_meters(feet):
    """
    Calculates approximate length in meters of input (feet)
    :param feet: length in ft
    :type feet: int or float
    :return: length in meters (approx)
    :rtype: float
    """
    m = feet / 3.281
    return m


def inches_to_meters(inches):
    """
    Calculates approximate length in meters of input (inches)
    :param inches: length in inches
    :type inches: int
    :return: length in meters
    :rtype: float
    """
    m = inches / 39.37
    return m


def inches_to_millimeter(inches):
    """
    Calculates millimeters from inches
    :param inches: length in inches
    :type inches: int
    :return: length in millimeters(mm)
    :rtype: float
    """
    mm = inches * 25.4
    return mm


class KöppenClimateClassifier:
    def __init__(self, prec_list:list, temp_list:list,
                 elevation=0, north=True):
        """
        Calculates Köppen Climate Classification
        of an area based on precipitation and temperature data,
        as well as location and elevation data, if known.
        :param prec_list: average precipitation measurements (in mm) for all 12 months in a given year
        :type prec_list: list[float]
        :param temp_list: average temperature measurements (in Celsius) for all 12 months in a given year
        :type temp_list: list[float]
        :param elevation: average elevation (only important if above 2300 meters) should be in meters
        :type elevation: int
        :param north: True if location is in northern hemisphere
        :type north: bool
        """
        self.elevation = elevation
        if north:
            self.hem = "N"
            self.winter = [9, 10, 11, 0, 1, 2]
            self.summer = [3, 4, 5, 6, 7, 8]
        else:
            self.hem = "S"
            self.winter = [3, 4, 5, 6, 7, 8]
            self.summer = [9, 10, 11, 0, 1, 2]
        if len(prec_list) == 12 and len(temp_list) == 12:
            self.temp_list = temp_list
            self.prec_list = prec_list
            self.MAT = sum(temp_list)/12
            self.MAP = sum(prec_list)/12
            self.Tcold = min(temp_list)
            self.Thot = max(temp_list)
            self.Tmon10 = 0
            for i in temp_list:
                if i >= 10:
                    self.Tmon10+=1
            self.Pw = [prec_list[i] for i in self.winter]
            self.Ps = [prec_list[i] for i in self.summer]
            self.Pdry = min(prec_list)
            self.Pwet = max(prec_list)
            self.Psdry = min(self.Ps)
            self.Pwwet = max(self.Pw)
            self.Pswet = max(self.Ps)
            self.Pwdry = min(self.Pw)
            if Psdry < Pwdry:
                self.dry_season = 'summer'
            else:
                self.dry_season = 'winter'
            self.dryness_factor = self.dry_factor()
            self.biome = self.biome_calc()
        else:
            raise ValueError("prec_list and temp_list should each contain 12 int or float values.")
    def dry_factor(self):
        """
        Calculates dryness factor needed for B climates
        :return:
        :rtype:
        """
        summer_total = sum(self.Ps)
        winter_total = sum(self.Pw)
        x = summer_total / self.MAP
        y = winter_total / self.MAP
        if x >= 0.7:
            dryness = self.MAT * 2 + 28
        elif y >= 0.7:
            dryness = self.MAT * 2
        else:
            dryness = self.MAT * 2 + 14
        return dryness

    def highlands(self):
        print('entered highlands')
        if self.elevation >= 2300:
            if self.Thot > 0:
                self.biome = 'HT'
                return self.biome
            else:
                self.biome = 'HF'
                return self.biome
        else:
            return self.polar()

    def polar(self):
        print('entered polar')
        if 0 < self.Thot <= 10:
            self.biome = 'ET'
            return self.biome
        elif self.Thot <= 0:
            self.biome = 'EF'
            return self.biome
        else:
            return self.arid()

    def arid(self):
        print('entered arid')
        if self.MAP < (10 * self.dryness_factor):
            if self.MAP < (5 * self.dryness_factor):
                if self.MAT >= 18:
                    self.biome = 'BWh'
                else:
                    self.biome = 'BWk'
            else:
                if self.MAT >= 18:
                    self.biome = 'BSh'
                else:
                    self.biome = 'BSk'
            return self.biome
        else:
            return self.tropical_or_cold()

    def tropical_or_cold(self):
        print('entered tropical_or_cold')
        if self.Tcold >= 18:
            return self.tropical()
        elif self.Tcold > -3:
            return self.warm_temperate()
        else:
            return self.cold_temperate()

    def tropical(self):
        print('entered tropical')
        if self.Pdry >= 60:
            self.biome = 'Af'
        elif self.Pdry >= (self.MAP - 25) * 100:
            self.biome = 'Am'
        elif self.dry_season == 'summer':
            self.biome = 'As'
        elif self.dry_season == 'winter':
            self.biome = 'Aw'
        else:
            self.biome = 'A'
        return self.biome

    def cold_temperate(self):
        print('entered cold_temperate')
        if self.Pwdry > self.Psdry:
            if self.Pwwet > self.Psdry * 3:
                if self.Psdry < 40:
                    self.biome = 'Ds'
        else:
            if self.Psdry > self.Pwdry:
                if self.Pswet > self.Pwdry * 10:
                    self.biome = 'Dw'
            else:
                self.biome = 'Df'
        return self.cold_temperate_summer()

    def cold_temperate_summer(self):
        print('cold_temperate_summer')
        if self.Thot >= 22:
            self.biome += 'a'
        elif self.Thot < 22 and self.Tmon10 >= 4:
            self.biome += 'b'
        elif self.Tmon10 < 4 and self.Tcold >= -38:
            self.biome += 'c'
        else:
            self.biome += 'd'
        return self.biome

    def warm_temperate(self):
        print('entered warm_temperate')
        if self.Pwdry > self.Psdry:
            if self.Pwwet > self.Psdry * 3:
                if self.Psdry < 40:
                    self.biome = 'Cs'
        if self.Psdry > self.Pwdry:
            if self.Pswet > self.Pwdry * 10:
                self.biome = 'Cw'
        else:
            self.biome = 'Cf'
        return self.warm_temperate_summer()

    def warm_temperate_summer(self):
        print('entered warm_temperate_summer')
        if self.Thot > 22:
            self.biome += 'a'
        elif self.Thot < 22 and self.Tmon10 >= 4:
            self.biome += 'b'
        else:
            self.biome += 'c'
        return self.biome

    def biome_calc(self):
        return self.highlands()


updated_temp_codes = dict(
    i=(35.0, 99.9),
    h=(28.0, 34.9),
    a=(23.0, 27.9),
    b=(18.0, 22.9),
    l=(10.0, 17.9),
    k=(0.1, 9.9),
    o=(-9.9, 0.0),
    c=(-24.9, -10.0),
    d=(-39.9, -25.0),
    e=(-99.9, -40.0)
)


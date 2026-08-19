class HeatingCurve:
    def __init__(self, table):
        """
        table: dict med {utetemp: framledningstemp}
        """
        self.points = sorted(table.items())

    def get(self, outdoor_temp):
        """
        Returnerar interpolerad framledningstemperatur.
        """
        if outdoor_temp <= self.points[0][0]:
            return self.points[0][1]

        if outdoor_temp >= self.points[-1][0]:
            return self.points[-1][1]

        for i in range(len(self.points) - 1):
            t1, f1 = self.points[i]
            t2, f2 = self.points[i + 1]

            if t1 <= outdoor_temp <= t2:
                ratio = (outdoor_temp - t1) / (t2 - t1)
                return f1 + ratio * (f2 - f1)

        return None

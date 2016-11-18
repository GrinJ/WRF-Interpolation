import numpy

class WRFInterpolation:

    def __init__(self, XLAT, XLON):
        """
        Allows to interpolate values from custom point to WRF model grid
        :param XLAT: Latitude array from CTLReader
        :type XLAT: numpy.array
        :param XLON: Longitide array from CTLReader
        :type XLON: numpy.array
        """

        # Save the grid values
        self.XLAT = XLAT
        self.XLON = XLON

        #Save the sizes
        self.__lat = len(XLAT)
        self.__lon = len(XLAT[0])

    def bilinear(self, ST_LAT, ST_LON, FIELD):
        """
        Simple bilinear interpolation
        :param ST_LAT: Point latitude
        :type ST_LAT: float
        :param ST_LON: Point longitude
        :type ST_LON: float
        :param FIELD: Custom field from CTLReader
        :type FIELD: numpy.array
        :return: Returns the interpolated value or -9999 if point is not in the grid
        :rtype:
        """

        #Get the values
        status, min_lat, max_lat, min_lon, max_lon = self.__firstInterpolate(ST_LON, ST_LAT)

        #Check the given status
        if status == True:

            #Return the interpolated value
            return self.__BilinearInterpolation(min_lat, max_lat, min_lon, max_lon, ST_LAT, ST_LON, FIELD)
        else:
            return -9999.0

    #Calculate simple bilinear interpolation using 4 points
    def __BilinearInterpolation(self, min_lat, max_lat, min_lon, max_lon, ST_LAT, ST_LON, FIELD):

        fR1 = FIELD[min_lat][min_lon] * (self.XLON[min_lat][max_lon] - ST_LON) / (self.XLON[min_lat][max_lon] - self.XLON[min_lat][min_lon]) + \
        FIELD[min_lat][max_lon] * (ST_LON - self.XLON[min_lat][min_lon]) / (self.XLON[min_lat][max_lon] - self.XLON[min_lat][min_lon])

        fR2 = FIELD[max_lat][min_lon] * (self.XLON[min_lat][max_lon] - ST_LON) / (self.XLON[min_lat][max_lon] - self.XLON[min_lat][min_lon]) + \
        FIELD[max_lat][max_lon] * (ST_LON - self.XLON[min_lat][min_lon]) / (self.XLON[min_lat][max_lon] - self.XLON[min_lat][min_lon])

        fP = fR1 * ( self.XLAT[max_lat][min_lon] - ST_LAT ) / ( self.XLAT[max_lat][min_lon] - self.XLAT[min_lat][min_lon] ) + \
        fR2 * ( ST_LAT - self.XLAT[min_lat][min_lon] ) / ( self.XLAT[max_lat][min_lon] - self.XLAT[min_lat][min_lon] )

        return fP


    #Tries at first time to find nearest points in array
    def __firstInterpolate(self, ST_LON, ST_LAT):

        #Calculate the step
        dLAT = numpy.fabs(self.XLON[0][1] - self.XLON[0][0]) * 3
        dLON = numpy.fabs(self.XLAT[1][0] - self.XLAT[0][0]) * 3

        #Get the rows and cells satisfying the condition
        rows, cells = numpy.where(((self.XLON >= ST_LON - dLON) & (self.XLON <= ST_LON + dLON)) & ((self.XLAT >= ST_LAT - dLAT) & (self.XLAT <= ST_LAT + dLAT)))

        #Loop through all the values
        for i in range(0, len(rows)):

            #Get the indexes
            current_lat = rows[i] if rows[i] != self.__lat - 1 else rows[i] - 1
            next_lat = rows[i] + 1 if rows[i] != self.__lat - 1 else rows[i]
            current_lon = cells[i] if cells[i] != self.__lon - 1 else cells[i] - 1
            next_lon = cells[i] + 1 if cells[i] != self.__lon - 1 else cells[i]

            #Check the point
            if ST_LON >= self.XLON[current_lat][current_lon] and ST_LON < self.XLON[current_lat][next_lon] and \
                ST_LAT >= self.XLAT[current_lat][current_lon] and ST_LAT < self.XLAT[next_lat][current_lon]:

                    return(True, current_lat, next_lat, current_lon, next_lon)

        #Return default value if point is not in our area
        return (False, 0, 0, 0, 0)
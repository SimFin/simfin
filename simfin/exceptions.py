##########################################################################
#
# Exceptions.
#
##########################################################################
# SimFin - Simple financial data for Python.
# www.simfin.com - www.github.com/simfin/simfin
# See README.md for instructions and LICENSE.txt for license details.
##########################################################################

class ServerException(Exception):
    """
    Exception for when the SimFin server returned an error.
    """

    def __init__(self, error):
        """
        :param error: String with the error message.
        """
        Exception.__init__(self, error)

##########################################################################


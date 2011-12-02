import traceback

class Error:
    def __init__(self, message=None):
        stack = traceback.extract_stack()
        origin_of_call      = stack[0]
        where_it_went_wrong = stack[1]

        if message:
            print message, "\n"

        print "Error in", origin_of_call[0], "on line", origin_of_call[1]
        print " : ", origin_of_call[3], "\n"

        # Inside try function, so -2 lines as exept and Error() are 2 lines
        print "Function called in", where_it_went_wrong[0]
        print "around line", (where_it_went_wrong[1] - 2), "\n"

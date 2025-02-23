import sys

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    ''' exc_info(): -> gives you 3 information, first 2 are not required but last third is giving you
                    -> on which file exception is occured?,
                    -> on which line number is occurred?,
                    -> which exceptiojn is occurred?,
                    all this info is giving by this variable'''
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}], line number [{1}] , error message [{2}]".format(
        file_name, exc_tb.tb_lineno,str(error)
    )
    return error_message

class customException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail = error_detail)

    def __str__(self):
        return self.error_message
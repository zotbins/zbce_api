
class Error(Exception):
    em = {"JSON_FORMAT": ("Request body is not in JSON format",400),
    "MISSING_KEY":("Missing key in body",400),
    "NULL_VALUE": ("Values cannot be null",400),
    "INVALID_PARAM": ("Invalid parameters",400),
    "INVALID_BIN_ID": ("Invalid bin_id",400),
    "INVALID_IP_ADDR": ("Invalid Ip Address",400),
    "IMAGE_EXISTS": ("Image already exists",400),
    "TIMESTAMP_ISSUE": ("start timestamp must be less than end timestamp",400)}
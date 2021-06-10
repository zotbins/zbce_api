"""
Resources:
- https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying
"""
# library imports
import datetime, time
import json
import requests

# local imports
from config import db, app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import models


def ip_valid(ip_addr: str) -> bool:
    """
    Checks whether or not the given ip-address exists in the database or not.
    If not, the function will return false.
    """
    bin = models.BinInfo.query.filter_by(ip_address=ip_addr).first()
    return bin != None


def ip_bin_id(ip_addr):
    """
    Returns the bin id, based on the given ip address.
    """
    bin = models.BinInfo.query.filter_by(ip_address=ip_addr).first()
    if bin == None:
        return None
    return bin.id

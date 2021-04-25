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
import error


def ip_valid(ip_addr:str)->bool:
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

def add_barcode_item(barcode: int, item_info: str, waste_bin: str):
    """
    Add to the barcode table
    """
    barcode_item = models.BarcodeItem.query.filter_by(barcode=barcode).first()
    if barcode_item:
        raise error.Error("DUPLICATE_BARCODE_ID")
    barcode_item = models.BarcodeItem(barcode=barcode,item=item_info,bin=waste_bin)
    db.session.add(barcode_item)
    db.session.commit()

def get_bin(barcode: int):
    """
    Queries for appropriate bin based on barcode
    """
    barcode_item = models.BarcodeItem.query.filter_by(barcode=barcode).first()
    if barcode_item == None:
        raise error.Error("BARCODE_NOT_FOUND")
    return barcode_item.bin

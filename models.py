# library imports
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, make_response, request, abort, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

# local imports
from config import db


class BinInfo(db.Model):
    __tablename__ = 'bins'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(64), unique=True)
    bin_height = db.Column(db.Integer)
    location = db.Column(db.String(64))
    bin_type = db.Column(db.String(64))
    waste_metrics = db.Column(db.String(64))

    fullnesses = db.relationship('BinFullness', backref='bin',lazy='dynamic')
    weights = db.relationship('BinWeight', backref='bin',lazy='dynamic')
    usages = db.relationship('BinUsage', backref='bin',lazy='dynamic')

    def __repr__(self):
        return '<BinInfo {}>'.format(self.id)

class BinFullness(db.Model):
    __tablename__ = 'fullness'

    id = db.Column(db.Integer, primary_key=True)
    datetimestamp = db.Column(db.DateTime)
    fullness = db.Column(db.Float)
    bin_id = db.Column(db.Integer,db.ForeignKey('bins.id'))

class BinWeight(db.Model):
    __tablename__ = 'weight'
    id = db.Column(db.Integer, primary_key=True)
    datetimestamp = db.Column(db.DateTime)
    bin_weight = db.Column(db.Float)
    bin_id = db.Column(db.Integer,db.ForeignKey('bins.id'))

class BinUsage(db.Model):
    __tablename__ = 'binusage'
    id = db.Column(db.Integer, primary_key=True)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    times_used= db.Column(db.Integer)
    bin_id = db.Column(db.Integer,db.ForeignKey('bins.id'))

from flask import Blueprint

web = Blueprint('web' , __name__)

from .view import *
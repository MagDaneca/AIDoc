# External Libraries
import pickle
import re
import tensorflow as tf
import numpy as np
from io import BytesIO
from datetime import timedelta, datetime
from datetime import *
import folium
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
from streamlit_login import __login__
from streamlit_login.utils import register_new_usr
from streamlit_modal import Modal
from pathlib import Path

# Local Utilities
from utils.database import *
from utils.different import *
from utils.doc import *
from utils.user import *
from utils.encdata import *
from utils.pharmacy import *
from utils.diseases import *

# Streamlit-specific
import streamlit as st
from streamlit_calendar1 import calendar

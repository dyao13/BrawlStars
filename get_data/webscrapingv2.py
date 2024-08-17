import sys
import io
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

original_stdout = sys.stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


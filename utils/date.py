
from datetime import datetime
def today():
    return datetime.now().strftime("%Y-%m-%d")

def year():
    return datetime.now().strftime("%Y")

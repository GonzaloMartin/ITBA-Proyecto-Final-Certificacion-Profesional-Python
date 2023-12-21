import warnings
import urllib3

def ignorarWarnings():
    warnings.simplefilter('ignore', ResourceWarning)
    urllib3.disable_warnings()

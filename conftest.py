import warnings
import urllib3

def ignorarWarnings():
    """
    Ignora los warnings de ResourceWarning y los deprecations de urllib3.
    Estos warnings son generados por el uso de la librería requests.

    :return: None
    """

    warnings.simplefilter('ignore', ResourceWarning)
    urllib3.disable_warnings()

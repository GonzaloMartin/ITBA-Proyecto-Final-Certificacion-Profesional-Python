import pytest
from src.proyecto import *

@pytest.mark.verificar_servicio
def test_verificar_servicio():
    """
    Verifica que el servicio de Polygon esté funcionando correctamente.
    Criterio de aceptación: El servicio debe responder con un código 200 y el servidor debe estar sincronizado.

    :return: None
    """
    response = get_verificar_servicio()
    assert response[0].status_code == 200, "El servicio no se ejecutó correctamente."
    assert str(get_anio()) in response[1]["serverTime"], "El servidor no está sincronizando."
    print("\nEl servicio Polygon de finanzas sincroniza correctamente. Iniciando el sistema.")

@pytest.mark.iniciar_sistema
def test_iniciar_sistema():
    """
    Inicia el sistema de finanzas.

    :return: None
    """
    iniciar_sistema()

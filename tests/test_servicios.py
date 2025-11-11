# tests/test_servicios.py

import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session
# Aseguramos que la importación use la ruta absoluta o relativa correcta
from backend.servicios import RepositorioVehiculos 
from backend.models import VehiculoBase, Vehiculo
from fastapi import HTTPException, status

# --- Fixture para simular la Sesión de Base de Datos ---

@pytest.fixture
def mock_db_session():
    """Crea un objeto simulado (mock) para la sesión de base de datos."""
    return MagicMock(spec=Session)

# --- Pruebas Unitarias para RepositorioVehiculos ---

def test_guardar_vehiculo_exitoso(mock_db_session):
    """
    Prueba que guardar_vehiculo() llame a los métodos de la base de datos (add, commit, refresh).
    """
    
    # Arrange (Preparación)
    repo = RepositorioVehiculos(mock_db_session)
    vehiculo_data = VehiculoBase(
        marca="Ford", 
        modelo="Ranger", 
        anio=2024, 
        dominio="ABC-123", 
        estado="disponible"
    )
    propietario_id = 1

    # Act (Ejecución)
    repo.guardar_vehiculo(vehiculo_data, propietario_id)

    # Assert (Verificación)
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_actualizar_estado_cambio_exitoso(mock_db_session):
    """
    Prueba que actualizar_estado() cambie correctamente el estado y guarde.
    """
    # Arrange (Preparación)
    repo = RepositorioVehiculos(mock_db_session)
    vehiculo_id = 1
    nuevo_estado = "en uso"
    
    # Simular un vehículo ya existente con estado 'disponible'
    vehiculo_mock = Mock(spec=Vehiculo, id=vehiculo_id, estado="disponible")
    mock_db_session.get.return_value = vehiculo_mock

    # Act (Ejecución)
    repo.actualizar_estado(vehiculo_id, nuevo_estado)

    # Assert (Verificación)
    assert vehiculo_mock.estado == "en uso"
    mock_db_session.commit.assert_called_once()


def test_actualizar_estado_con_estado_invalido(mock_db_session):
    """
    Prueba que actualizar_estado() maneje estados inválidos levantando una excepción.
    Esto verifica la lógica de negocio.
    """
    # Arrange (Preparación)
    repo = RepositorioVehiculos(mock_db_session)
    vehiculo_id = 1
    estado_invalido = "destruido" 
    
    vehiculo_mock = Mock(spec=Vehiculo, id=vehiculo_id, estado="disponible")
    mock_db_session.get.return_value = vehiculo_mock

    # Act & Assert (Ejecución y Verificación)
    # Se espera que el método lance una HTTPException (error 400)
    with pytest.raises(HTTPException) as excinfo:
        repo.actualizar_estado(vehiculo_id, estado_invalido)

    # Verificar el código y el mensaje de error
    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Estado inválido" in str(excinfo.value.detail)
    
    # Asegurar que NUNCA se hizo commit a la base de datos
    mock_db_session.commit.assert_not_called()
// frontend/src/pages/VehicleList.jsx
// frontend/src/pages/VehicleList.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Dependencia para las peticiones HTTP

// Funciones básicas para la lista
function VehicleList() {
    const [vehicles, setVehicles] = useState([]);
    const [loading, setLoading] = useState(true);

    // Función de obtención de datos (llamada repetidamente, ¡cuidado con la eficiencia!)
    const fetchVehicles = async () => {
        try {
            // URL quemada directamente en el código
            const response = await axios.get('http://127.0.0.1:8000/api/vehiculos'); 
            setVehicles(response.data);
        } catch (error) {
            console.error("Error al obtener la lista de vehículos:", error);
            // Manejo de error simple
            setVehicles([]);
        } finally {
            setLoading(false);
        }
    };

    // [Función de Actualización de Estado (Lógica mezclada)]
    const handleUpdateState = async (vehiculoId, nuevoEstado) => {
        try {
            // Se usa el endpoint PATCH /api/vehiculos/{id}/estado (Requisito 3)
            await axios.patch(`http://127.0.0.1:8000/api/vehiculos/${vehiculoId}/estado?nuevo_estado=${nuevoEstado}`);
            
            // Retroalimentación simple de alerta
            alert(`Estado del vehículo ID ${vehiculoId} cambiado a ${nuevoEstado}. ¡Listo!`);
            
            // Recargar la lista (Llamar de nuevo a fetchVehicles es la forma más simple)
            fetchVehicles(); 

        } catch (error) {
            console.error("Error al actualizar el estado:", error.response ? error.response.data : error.message);
            alert("Error al actualizar el estado. Revisa la consola.");
        }
    };
    
    // Llamada inicial (se hace una vez, pero la función se llama muchas veces después)
    useEffect(() => {
        fetchVehicles();
    }, []);

    if (loading) return <div style={{ padding: '20px', color: 'black' }}>Cargando... ¡Espera!</div>;

    return (
        // Estilos corregidos para la visibilidad (fondo blanco y texto negro)
        <div style={{ padding: '20px', border: '2px solid black', minWidth: '550px', margin: '10px', backgroundColor: 'white', color: 'black' }}>
            <h2>2 & 3. Lista de Flota y Cambio de Estado</h2> 
            
            {/* Mensaje de no vehículos */}
            {vehicles.length === 0 && <p style={{ color: 'blue' }}>No hay vehículos registrados aún.</p>}

            {/* Listado condicional */}
            {vehicles.length > 0 && (
                <div>
                    <h3>Flota Activa ({vehicles.length}):</h3>
                    <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
                        {vehicles.map(v => (
                            <li key={v.dominio} style={{ margin: '15px 0', border: '1px solid #ccc', padding: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#f0f0f0' }}>
                                
                                {/* Información del Vehículo */}
                                <div>
                                    <p style={{ margin: '0' }}><strong>{v.marca} {v.modelo}</strong> ({v.dominio})</p>
                                    <p style={{ margin: '0', fontWeight: 'bold' }}>Estado Actual: {v.estado.toUpperCase()}</p>
                                </div>
                                
                                {/* Botones de acción (Requisito 3) */}
                                <div>
                                    {v.estado !== 'en uso' && (
                                        <button 
                                            onClick={() => handleUpdateState(v.id, 'en uso')} 
                                            style={{ background: '#007bff', color: 'white', border: '1px solid black', padding: '5px 10px', cursor: 'pointer', marginRight: '10px' }}
                                        >
                                            Pasar a EN USO
                                        </button>
                                    )}
                                    {v.estado !== 'mantenimiento' && (
                                        <button 
                                            onClick={() => handleUpdateState(v.id, 'mantenimiento')} 
                                            style={{ background: 'darkgray', color: 'white', border: '1px solid black', padding: '5px 10px', cursor: 'pointer' }}
                                        >
                                            MANDAR A MANTENIMIENTO
                                        </button>
                                    )}
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default VehicleList;
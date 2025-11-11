// frontend/src/pages/MaintenanceForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

const MaintenanceForm = () => {
    // Estado único para capturar los datos y el ID
    const [vehiculoId, setVehiculoId] = useState('');
    const [tipo, setTipo] = useState('preventivo');
    const [notas, setNotas] = useState('');
    const [maintenanceHistory, setMaintenanceHistory] = useState([]);
    const [feedback, setFeedback] = useState('');

    // Función para registrar un nuevo mantenimiento (POST)
    const handleRegisterMaintenance = async (e) => {
        e.preventDefault();
        setFeedback('');

        if (!vehiculoId) {
            setFeedback("ERROR: Debes ingresar un ID de vehículo para registrar.");
            return;
        }

        try {
            const data = { tipo, notas };
            // Endpoint POST para registro (Requisito 4)
            await axios.post(`http://127.0.0.1:8000/api/vehiculos/${vehiculoId}/mantenimientos`, data);
            
            setFeedback(`Mantenimiento registrado para ID ${vehiculoId}.`);
            setNotas('');
            
            // Llama a la función de consulta después de registrar, de forma directa
            handleFetchHistory(); 

        } catch (err) {
            console.error("Error al registrar:", err.response ? err.response.data : err.message);
            setFeedback('ERROR al registrar: Verifica que el ID del vehículo exista.');
        }
    };

    // Función para consultar el historial (GET)
    const handleFetchHistory = async () => {
        setFeedback('');
        if (!vehiculoId) {
            setFeedback("ERROR: Ingresa un ID de vehículo para consultar.");
            setMaintenanceHistory([]);
            return;
        }

        try {
            // Endpoint GET para consultar el historial (Requisito 5)
            const response = await axios.get(`http://127.0.0.1:8000/api/vehiculos/${vehiculoId}/mantenimientos`);
            setMaintenanceHistory(response.data);
            setFeedback(`Historial encontrado para vehículo ID ${vehiculoId}.`);
            
        } catch (err) {
            console.error("Error al consultar:", err.response ? err.response.data : err.message);
            setFeedback('ERROR al consultar: ID no encontrado o Backend caído.');
            setMaintenanceHistory([]);
        }
    };

    // --- Interfaz ---
    return (
        <div style={{ padding: '20px', border: '1px solid #000', minWidth: '400px', margin: '20px', backgroundColor: '#f0f0f0' }}>
            <h2>4 & 5. Registro y Historial de Mantenimiento</h2>
            
            <label style={{ display: 'block', margin: '10px 0 5px' }}>ID del Vehículo:</label>
            <input 
                type="number" 
                value={vehiculoId} 
                onChange={(e) => setVehiculoId(e.target.value)} 
                placeholder="ID del Vehículo (Ej: 1)" 
            />
            
            <p style={{ color: feedback.startsWith('ERROR') ? 'red' : 'green', fontWeight: 'bold' }}>{feedback}</p>
            
            {/* Formulario de Registro */}
            <h3>Registrar Evento (POST)</h3>
            <form onSubmit={handleRegisterMaintenance}>
                <label>Tipo:</label>
                <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
                    <option value="preventivo">Preventivo</option>
                    <option value="correctivo">Correctivo</option>
                    <option value="revision">Revisión</option>
                </select>

                <label>Notas:</label>
                <textarea value={notas} onChange={(e) => setNotas(e.target.value)}></textarea>

                <button type="submit" style={{ background: 'darkblue', color: 'white', marginTop: '10px' }}>
                    Registrar Mantenimiento
                </button>
            </form>

            {/* Consulta y Historial */}
            <h3 style={{ marginTop: '30px' }}>Consultar Historial (GET)</h3>
            <button onClick={handleFetchHistory} style={{ background: 'gray', color: 'white', marginBottom: '15px' }}>
                Consultar Historial por ID
            </button>

            {maintenanceHistory.length > 0 && (
                <div style={{ border: '1px solid #ccc', padding: '10px', backgroundColor: 'white' }}>
                    <h4>Historial Encontrado:</h4>
                    {maintenanceHistory.map((m, index) => (
                        <p key={index}>
                            - {new Date(m.fecha).toLocaleDateString()}: {m.tipo.toUpperCase()}
                        </p>
                    ))}
                </div>
            )}
        </div>
    );
};

export default MaintenanceForm;
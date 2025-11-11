// frontend/src/pages/VehicleForm.jsx
import React, { useState } from 'react';
import axios from 'axios'; 

// Definición COMPLETA del componente VehicleForm
const VehicleForm = ({ onVehicleRegistered }) => { 
    // 1. Estados
    const [marca, setMarca] = useState('');
    const [modelo, setModelo] = useState('');
    const [anio, setAnio] = useState(2025); 
    const [dominio, setDominio] = useState('');
    const [estado, setEstado] = useState('disponible'); 

    // 2. Estados para el feedback
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    // Función principal para el envío de datos
    const handleSubmit = async (e) => {
        e.preventDefault(); 
        
        setMessage('');
        setError('');

        const formData = {
            marca: marca,
            modelo: modelo,
            anio: parseInt(anio), 
            dominio: dominio,
            estado: estado 
        };

        try {
            // Envía los datos al endpoint POST /api/vehiculos
            await axios.post('http://127.0.0.1:8000/api/vehiculos', formData);
            
            setMessage(`¡ÉXITO! Vehículo registrado.`);
            
            // Limpiar campos
            setMarca('');
            setModelo('');
            setAnio(2025);
            setDominio('');
            setEstado('disponible');

            if (onVehicleRegistered) {
                onVehicleRegistered();
            }

        } catch (err) {
            console.error("Error de registro:", err.response ? err.response.data : err.message);
            setError('ERROR: Falló el registro. ¿Matrícula ya existe o API no responde?');
        }
    };

    // <--- INICIO DEL BLOQUE RETURN CORREGIDO --->
    return (
        <div style={{ padding: '20px', border: '2px solid black', maxWidth: '450px', margin: '10px', backgroundColor: '#fffbe0', color: 'black' }}>
            
            <h2>1. Formulario de Registro (POST)</h2> 
            
            {message && <p style={{ color: 'green', fontWeight: 'bold' }}>{message}</p>}
            {error && <p style={{ color: 'red', fontWeight: 'bold' }}>{error}</p>}

            <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '10px', alignItems: 'center' }}>
                
                <label style={{color: 'black'}}>Marca:</label>
                <input type="text" value={marca} onChange={(e) => setMarca(e.target.value)} required />
                
                <label style={{color: 'black'}}>Modelo:</label>
                <input type="text" value={modelo} onChange={(e) => setModelo(e.target.value)} required />
                
                <label style={{color: 'black'}}>Año:</label>
                <input type="number" value={anio} onChange={(e) => setAnio(e.target.value)} min="1950" required />
                
                <label style={{color: 'black'}}>Matrícula (Dominio):</label>
                <input type="text" value={dominio} onChange={(e) => setDominio(e.target.value)} required />
                
                <label style={{color: 'black'}}>Estado Inicial:</label>
                <select value={estado} onChange={(e) => setEstado(e.target.value)}>
                    <option value="disponible">Disponible</option>
                    <option value="en uso">En Uso</option>
                    <option value="mantenimiento">Mantenimiento</option>
                </select>

                <button type="submit" style={{ gridColumn: 'span 2', marginTop: '20px', padding: '10px', background: 'darkgreen', color: 'white' }}>
                    REGISTRAR VEHÍCULO EN FLOTA
                </button>
            </form>
        </div>
    );
}; // <--- La llave de cierre del componente

export default VehicleForm;
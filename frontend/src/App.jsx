// frontend/src/App.jsx
import React, { useState } from 'react';
import VehicleList from './pages/VehicleList'; 
import VehicleForm from './pages/VehicleForm'; 
import MaintenanceForm from './pages/MaintenanceForm'; 
// No necesita App.css, pero lo dejamos si existe para evitar errores

function App() {
    // Clave para forzar la actualización de la lista de vehículos después del registro
    const [listKey, setListKey] = useState(0);

    const handleVehicleRegistered = () => {
        // Incrementa la clave para forzar a VehicleList a recargar los datos (Solución 'newbie' para recargar)
        setListKey(prevKey => prevKey + 1);
    };

    return (
        <div style={{ display: 'flex', gap: '30px', padding: '10px', fontFamily: 'Arial, sans-serif' }}>
            
            {/* Columna de Registro y Mantenimiento */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <VehicleForm onVehicleRegistered={handleVehicleRegistered} />
                <MaintenanceForm /> 
            </div>
            
            {/* Columna de Listado y Actualización (key={listKey} fuerza la recarga) */}
            <VehicleList key={listKey} />

        </div>
    );
}

export default App;

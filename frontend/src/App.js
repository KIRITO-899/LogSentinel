import React, { useState, useEffect, useMemo } from 'react';
import { io } from 'socket.io-client';
import { DataGrid } from '@mui/x-data-grid';
import LogChart from './components/LogChart';
import TimeChart from './components/TimeChart';
import Alerts from './components/Alerts';
import './App.css';

// Construct the socket using the proxy or current domain
const socket = io();

function App() {
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logTypeFilter, setLogTypeFilter] = useState('');
  const [processNameFilter, setProcessNameFilter] = useState('');

  useEffect(() => {
    socket.on('initial_data', (data) => {
      setLogs(data.logs);
      setAlerts(data.alerts);
    });

    socket.on('new_log', (log) => {
      setLogs((prevLogs) => {
        const updatedLogs = [...prevLogs, log];
        return updatedLogs.length > 1000 ? updatedLogs.slice(-1000) : updatedLogs;
      });
    });

    socket.on('update_alerts', (newAlerts) => {
      setAlerts(newAlerts);
    });

    return () => {
      socket.off('initial_data');
      socket.off('new_log');
      socket.off('update_alerts');
    };
  }, []);

  const filteredLogs = useMemo(() => {
    return logs.filter(log => {
      const logTypeMatch = log.log_type.toLowerCase().includes(logTypeFilter.toLowerCase());
      const processNameMatch = log.process_name.toLowerCase().includes(processNameFilter.toLowerCase());
      return logTypeMatch && processNameMatch;
    });
  }, [logs, logTypeFilter, processNameFilter]);

  const columns = [
    { field: 'timestamp', headerName: 'Timestamp', width: 200 },
    { field: 'hostname', headerName: 'Hostname', width: 150 },
    { field: 'log_type', headerName: 'Log Type', width: 120 },
    { field: 'severity', headerName: 'Severity', width: 100 },
    { field: 'process_name', headerName: 'Process Name', width: 200 },
    { field: 'source_ip', headerName: 'Source IP', width: 150 },
    { field: 'message', headerName: 'Message', width: 500 },
  ];

  return (
    <div className="App" style={{ width: '100%' }}>
      <h1>LogSentinel Real-Time</h1>
      <Alerts alerts={alerts} />
      
      <h2>Filters</h2>
      <div style={{ marginBottom: '10px' }}>
        <input
          type="text"
          placeholder="Filter by Log Type"
          value={logTypeFilter}
          onChange={e => setLogTypeFilter(e.target.value)}
          style={{ marginRight: '10px' }}
        />
        <input
          type="text"
          placeholder="Filter by Process Name"
          value={processNameFilter}
          onChange={e => setProcessNameFilter(e.target.value)}
        />
      </div>

      <LogChart data={filteredLogs} />
      <h2>Events Over Time</h2>
      <TimeChart data={filteredLogs} />
      <div style={{ height: 400, width: '100%', marginTop: '20px' }}>
        <DataGrid
          rows={filteredLogs}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 5, page: 0 },
            },
          }}
          pageSizeOptions={[5, 10, 25]}
          checkboxSelection
        />
      </div>
    </div>
  );
}

export default App;

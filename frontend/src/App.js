import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { DataGrid } from '@mui/x-data-grid';
import LogChart from './components/LogChart';
import TimeChart from './components/TimeChart';
import Alerts from './components/Alerts';
import './App.css';

function App() {
  const [logs, setLogs] = useState([]);
  const [logTypeFilter, setLogTypeFilter] = useState('');
  const [processNameFilter, setProcessNameFilter] = useState('');

  useEffect(() => {
    const fetchLogs = () => {
      axios.get('/api/logs')
        .then(response => {
          const logsWithIds = response.data.map((log, index) => ({
            ...log,
            id: index,
          }));
          setLogs(logsWithIds);
        })
        .catch(error => {
          console.error('Error fetching logs:', error);
        });
    };

    fetchLogs(); // Initial fetch
    const intervalId = setInterval(fetchLogs, 5000); // Fetch every 5 seconds

    return () => clearInterval(intervalId); // Cleanup on component unmount
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
      <h1>LogSentinel</h1>
      <Alerts />
      
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
          pageSize={5}
          rowsPerPageOptions={[5]}
          checkboxSelection
        />
      </div>
    </div>
  );
}

export default App;

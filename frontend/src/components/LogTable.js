import React from 'react';

const LogTable = ({ logs }) => {
  if (!logs || logs.length === 0) {
    return <p>No logs to display.</p>;
  }

  return (
    <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
      <h2>All Logs</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid black' }}>
            <th style={{ textAlign: 'left', padding: '8px' }}>Timestamp</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Process Name</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Severity</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Source IP</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Message</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: '8px' }}>{log.timestamp}</td>
              <td style={{ padding: '8px' }}>{log.process_name}</td>
              <td style={{ padding: '8px' }}>{log.severity}</td>
              <td style={{ padding: '8px' }}>{log.source_ip}</td>
              <td style={{ padding: '8px' }}>{log.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LogTable;

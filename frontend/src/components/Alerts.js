import React from 'react';

const Alerts = ({ alerts }) => {
  if (!alerts || alerts.length === 0) {
    return null;
  }

  return (
    <div>
      <h2>Security Alerts</h2>
      <ul>
        {alerts.map((alert, index) => (
          <li key={index}>
            <strong>{alert.type}:</strong> {alert.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Alerts;

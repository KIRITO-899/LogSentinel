import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    axios.get('/api/alerts')
      .then(response => {
        setAlerts(response.data);
      })
      .catch(error => {
        console.error('Error fetching alerts:', error);
      });
  }, []);

  if (alerts.length === 0) {
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

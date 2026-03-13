import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const LogChart = ({ data }) => {
  // Process data to count logs per process name
  const processCounts = data.reduce((acc, log) => {
    const processName = log.process_name || 'unknown';
    acc[processName] = (acc[processName] || 0) + 1;
    return acc;
  }, {});

  const chartData = Object.keys(processCounts).map(processName => ({
    name: processName,
    count: processCounts[processName],
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        data={chartData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default LogChart;

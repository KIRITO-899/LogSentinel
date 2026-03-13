import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TimeChart = ({ data }) => {
  // Process data to count logs per minute
  const eventsPerMinute = data.reduce((acc, log) => {
    try {
      // The log timestamp is like "Mar 12 10:45:01". The year is missing.
      // We'll add the current year to make it a valid date.
      const currentYear = new Date().getFullYear();
      const date = new Date(`${log.timestamp} ${currentYear}`);
      
      // Normalize the date to the minute
      const minute = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes()).toISOString();
      
      acc[minute] = (acc[minute] || 0) + 1;
    } catch (e) {
      console.error("Error parsing date for log:", log, e);
    }
    return acc;
  }, {});

  const chartData = Object.keys(eventsPerMinute)
    .sort() // Sort the minutes chronologically
    .map(minute => ({
      time: new Date(minute).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      count: eventsPerMinute[minute],
    }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
        data={chartData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="count" stroke="#82ca9d" name="Events per minute" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TimeChart;

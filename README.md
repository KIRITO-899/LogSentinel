# LogSentinel: A Web-Based Log Analysis Dashboard

## Introduction

LogSentinel is a powerful and intuitive web-based log analysis dashboard designed to provide a comprehensive overview of system logs. It helps users to monitor, analyze, and visualize log data in real-time, enabling them to quickly identify and respond to potential security threats and system issues.

## Features

*   **Real-time Log Analysis:** Ingests and processes `auth.log` and `syslog.log` files in real-time.
*   **Interactive Dashboard:** A user-friendly and interactive dashboard for log visualization and analysis.
*   **Threat Detection:** Automatically detects potential security threats, such as multiple failed login attempts.
*   **Data Visualization:** Includes a variety of charts and graphs to visualize log data, such as logs per process and events over time.
*   **Filtering and Searching:** Powerful filtering and searching capabilities to quickly find the information you need.
*   **Alerts:** Real-time alerts to notify users of potential security threats.

## Architecture

LogSentinel follows a client-server architecture, with a React-based frontend and a Python-based backend.

### Backend

The backend is built with the Flask framework and is responsible for the following:

*   **Log Parsing:** It parses `auth.log` and `syslog.log` files to extract key information, including:
    *   Timestamp
    *   Hostname
    *   Process Name
    *   Message
    *   Source IP
    *   Severity
*   **Threat Detection:** The `threat_detector.py` module analyzes the logs for potential security threats. Currently, it detects multiple failed login attempts from the same IP address.
*   **API Endpoints:** The backend exposes the following API endpoints:
    *   `/api/logs`: Returns all the parsed logs.
    *   `/api/alerts`: Returns a list of security alerts detected from the logs.

### Frontend

The frontend is a single-page application built with React. It provides a dynamic and interactive dashboard for log analysis and visualization. The key components of the frontend include:

*   **Alerts:** Displays real-time security alerts.
*   **Filters:** Enables users to filter logs by log type and process name.
*   **LogChart:** A bar chart that visualizes the distribution of logs per process name.
*   **TimeChart:** A line chart that shows the trend of log events over time.
*   **LogTable:** A comprehensive table of all log entries, with features for sorting and filtering.

The frontend uses the following libraries:

*   **Recharts:** For creating interactive charts and graphs.
*   **@mui/x-data-grid:** For creating a powerful and feature-rich data grid.

## How to Run

To run the application, follow these steps:

1.  **Start the backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    python app.py
    ```
2.  **Start the frontend:**
    ```bash
    cd frontend
    npm install
    npm start
    ```

The application will then be accessible at `http://localhost:3000`.
# LogSentinel
# Logsentinel

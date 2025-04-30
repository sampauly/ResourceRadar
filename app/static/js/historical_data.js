document.addEventListener('DOMContentLoaded', function() {
    console.log('Historical data JavaScript loaded');

    const serverSelect = document.getElementById('server-id');
    const fetchButton = document.getElementById('fetch-btn');
    const loadingContainer = document.getElementById('loading-container');
    const errorContainer = document.getElementById('error-container');

    let chartInstance = null;

    // Hardcoded servers - consider replacing with API call
    const servers = [
        { id: 'server_1', name: 'Server 1' },
        { id: 'server_2', name: 'Server 2' },
    ];

    servers.forEach(server => {
        const option = document.createElement('option');
        option.value = server.id;
        option.textContent = server.name;
        serverSelect.appendChild(option);
    });

    // Set default time range (last 24 hours)
    function setDefaultTimeRange() {
        const now = new Date();
        const yesterday = new Date(now);
        yesterday.setDate(yesterday.getDate() - 1);
        
        document.getElementById('end-time').value = now.toISOString().slice(0, 16);
        document.getElementById('start-time').value = yesterday.toISOString().slice(0, 16);
    }
    
    // Initialize with default time range
    setDefaultTimeRange();

    fetchButton.addEventListener('click', function() {
        const metricType = document.getElementById('metric-type').value;
        const serverId = document.getElementById('server-id').value;
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;

        console.log(`Fetching data for ${metricType} on ${serverId} from ${startTime} to ${endTime}`);

        // Show loading indicator and hide any previous errors
        loadingContainer.style.display = 'block';
        errorContainer.style.display = 'none';
    
        fetch('/api/historical_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                metric: metricType,
                server: serverId,
                start_time: startTime,
                end_time: endTime
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`Server error ${response.status}: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            loadingContainer.style.display = 'none';
            if (data.error) {
                console.error('API error:', data.error);
                showError('Error fetching data: ' + data.error);
            } else {
                console.log('Received data:', data);
                
                // Check the structure of the data
                if (!data.timestamps && data.labels) {
                    // If data has 'labels' instead of 'timestamps'
                    data.timestamps = data.labels;
                }
                
                if (metricType === 'network') {
                    if (data.sent && data.received) {
                        renderNetworkChart(data.timestamps, data.sent, data.received, serverId);
                    } else {
                        showError('Invalid data format for network metrics');
                    }
                } else {
                    // Handle both possible data formats
                    if (Array.isArray(data.values)) {
                        // If values is an array of arrays, take the first one
                        const values = Array.isArray(data.values[0]) ? data.values[0] : data.values;
                        renderChart(data.timestamps, values, `${metricType} on ${serverId}`);
                    } else if (data.values) {
                        // If values is a direct property
                        renderChart(data.timestamps, data.values, `${metricType} on ${serverId}`);
                    } else {
                        showError('Invalid data format: No values found');
                    }
                }
            }
        })
        .catch(error => {
            loadingContainer.style.display = 'none';
            console.error('Fetch error:', error);
            showError('Failed to fetch data: ' + error.message);
        });
    });

    function showError(message) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    }

    function formatTimestamps(timestamps) {
        return timestamps.map(timestamp => {
            // Check if timestamp is already a formatted string
            if (typeof timestamp === 'string' && !timestamp.includes('T')) {
                return timestamp;
            }
            
            const date = new Date(timestamp);
            return date.toLocaleString();
        });
    }

    function renderChart(timestamps, values, chartLabel) {
        const ctx = document.getElementById('historical-chart').getContext('2d');
        const formattedLabels = formatTimestamps(timestamps);

        console.log('Rendering chart with labels:', formattedLabels);
        console.log('and values:', values);

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedLabels,
                datasets: [{
                    label: chartLabel,
                    data: values,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            title: function(tooltipItem) {
                                return tooltipItem[0].label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: chartLabel
                        }
                    }
                }
            }
        });
    }

    function renderNetworkChart(timestamps, sentValues, receivedValues, serverId) {
        const ctx = document.getElementById('historical-chart').getContext('2d');
        const formattedLabels = formatTimestamps(timestamps);
        
        console.log('Rendering network chart with labels:', formattedLabels);
        console.log('Sent values:', sentValues);
        console.log('Received values:', receivedValues);
    
        if (chartInstance) {
            chartInstance.destroy();
        }
    
        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedLabels,
                datasets: [
                    {
                        label: `Network Sent on ${serverId}`,
                        data: sentValues,
                        borderColor: 'rgb(255, 99, 132)',
                        fill: false,
                        tension: 0.1
                    },
                    {
                        label: `Network Received on ${serverId}`,
                        data: receivedValues,
                        borderColor: 'rgb(54, 162, 235)',
                        fill: false,
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Network Usage (kbit/s)'
                        }
                    }
                }
            }
        });
    }
});
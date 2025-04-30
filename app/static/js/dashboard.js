// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing dashboard...");
    
    // Get references to containers
    const chartsContainer = document.getElementById('charts-container');
    const errorContainer = document.getElementById('error-container');
    
    if (!chartsContainer) {
        console.error("Charts container not found!");
        return; // Exit if we can't find the container
    }
    
    // Show loading message
    chartsContainer.innerHTML = '<div class="loading">Loading metrics data...</div>';
    
    // Fetch current metrics data
    fetchMetrics();
    
    // Function to fetch metrics data
    function fetchMetrics() {
        console.log("Fetching metrics data...");
        
        fetch('/api/current_metrics')
            .then(response => {
                console.log(`API response status: ${response.status}`);
                
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || `Server error: ${response.status}`);
                    });
                }
                
                return response.json();
            })
            .then(data => {
                console.log("Metrics data received:", data);
                
                // Hide any previous error
                if (errorContainer) {
                    errorContainer.style.display = 'none';
                }
                
                // Check if data is empty
                if (Object.keys(data).length === 0) {
                    throw new Error("No metrics data available");
                }
                
                // Create charts with the data
                createDashboard(data);
            })
            .catch(error => {
                console.error("Error fetching metrics:", error);
                
                // Show error message
                if (errorContainer) {
                    errorContainer.style.display = 'block';
                    errorContainer.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Error:</strong> ${error.message}
                        </div>
                    `;
                }
                
                // Clear loading message
                chartsContainer.innerHTML = '';
            });
    }
    
    // Function to create the dashboard
    function createDashboard(data) {
        // Clear the container
        chartsContainer.innerHTML = '';
        
        // Create a section for each server
        Object.keys(data).forEach(serverName => {
            const metrics = data[serverName];
            
            // Create server section
            const serverSection = document.createElement('div');
            serverSection.className = 'server-section';
            
            // Create header
            const header = document.createElement('h2');
            const serverIndex = Object.keys(data).indexOf(serverName) + 1;
            header.textContent = `Server ${serverIndex}`;
            serverSection.appendChild(header);
            
            // Create grid for charts
            const chartGrid = document.createElement('div');
            chartGrid.className = 'chart-grid';
            
            // Create charts for each metric
            const metrics_data = [
                { name: 'CPU Usage', value: metrics.cpu_usage, id: 'cpu', unit: '%' },
                { name: 'Disk Usage', value: metrics.disk_usage, id: 'disk', unit: '%' },
                { name: 'Memory Usage', value: metrics.memory_usage, id: 'memory', unit: '%' },
            ];
            
            metrics_data.forEach(metric => {
                const chartContainer = document.createElement('div');
                chartContainer.className = 'chart-container';
                
                const canvas = document.createElement('canvas');
                canvas.id = `${serverName}-${metric.id}-chart`;
                chartContainer.appendChild(canvas);
                
                const label = document.createElement('div');
                label.className = 'chart-label';
                label.textContent = `${metric.name}: ${metric.value}${metric.unit}`;
                chartContainer.appendChild(label);
                
                chartGrid.appendChild(chartContainer);
                
                // Schedule chart creation (to ensure canvas is in DOM)
                setTimeout(() => {
                    createGaugeChart(canvas.id, metric.value);
                }, 0);
            });

            if (metrics.network_sent !== undefined && metrics.network_received !== undefined) {
                const chartContainer = document.createElement('div');
                chartContainer.className = 'chart-container';
            
                const canvas = document.createElement('canvas');
                const barChartId = `${serverName}-network-bar-chart`;
                canvas.id = barChartId;
                chartContainer.appendChild(canvas);

                canvas.id = barChartId;
                canvas.classList.add('bar-chart'); // optional class for CSS targeting
                canvas.height = 250; // Adjust height to match gauge chart
                chartContainer.appendChild(canvas);
            
                const label = document.createElement('div');
                label.className = 'chart-label';
                label.textContent = `Network Sent: ${metrics.network_sent} kbit/s\n Network Received: ${metrics.network_received} kbit/s`;
                chartContainer.appendChild(label);
            
                chartGrid.appendChild(chartContainer);
            
                setTimeout(() => {
                    createBarChart(barChartId, metrics.network_sent, metrics.network_received);
                }, 0);
            }
            
            serverSection.appendChild(chartGrid);
            chartsContainer.appendChild(serverSection);
        });
    }
    
    // Function to create a gauge chart
    function createGaugeChart(canvasId, value) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element ${canvasId} not found`);
            return;
        }
        
        // Ensure value is a number and between 0-100
        const numValue = parseFloat(value);
        const safeValue = isNaN(numValue) ? 0 : Math.min(Math.max(numValue, 0), 100);
        
        let color;
        if (safeValue > 80) {
            color = '#e74c3c'; // Bright Red
        } else if (safeValue > 60) {
            color = '#f39c12'; // Orange
        } else if (safeValue > 40) {
            color = '#27ae60'; // Emerald
        } else {
            color = '#3498db'; // Blue
        }
        // Create chart
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [safeValue, 100 - safeValue],
                    backgroundColor: [color, 'rgba(220, 220, 220, 0.3)'],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '70%',
                circumference: 180,
                rotation: -90,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                responsive: true,
                maintainAspectRatio: true,
                plugins: [{
                    id: 'center-text',
                    beforeDraw: chart => {
                        const ctx = chart.ctx;
                        const width = chart.width;
                        const height = chart.height;
                        ctx.restore();
                        const fontSize = (height / 114).toFixed(2);
                        ctx.font = fontSize + "em sans-serif";
                        ctx.textBaseline = "middle";
                        const text = `${safeValue.toFixed(0)}%`;
                        const textX = Math.round((width - ctx.measureText(text).width) / 2);
                        const textY = height / 1.6;
                        ctx.fillText(text, textX, textY);
                        ctx.save();
                    }
                }]
            }
        });
    }

    function createBarChart(canvasId, sent, received) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) {
            console.error(`Canvas element ${canvasId} not found`);
            return;
        }
    
        const safeSent = isNaN(parseFloat(sent)) ? 0 : parseFloat(sent);
        const safeReceived = isNaN(parseFloat(received)) ? 0 : parseFloat(received);
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Sent', 'Received'],
                datasets: [{
                    label: 'Network Traffic (kbit/s)',
                    data: [safeSent, safeReceived],
                    backgroundColor: ['#2980b9', '#d35400'], // Blue & Orange
                    borderRadius: 4,
                    borderSkipped: false,
                    barThickness: 40,
                    borderRadius: 6
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: Math.max(10, Math.ceil(Math.max(safeSent, safeReceived) / 4))
                        },
                        title: {
                            display: true,
                            text: 'kbit/s'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true
                    }
                },
                responsive: true,
                maintainAspectRatio: true
            }
        });
    }
    
});
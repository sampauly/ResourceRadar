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
            header.textContent = `Server: ${serverName}`;
            serverSection.appendChild(header);
            
            // Create grid for charts
            const chartGrid = document.createElement('div');
            chartGrid.className = 'chart-grid';
            
            // Create charts for each metric
            const metrics_data = [
                { name: 'CPU Usage', value: metrics.cpu_usage, id: 'cpu', unit: '%' },
                { name: 'Disk Usage', value: metrics.disk_usage, id: 'disk', unit: '%' },
                { name: 'Memory Usage', value: metrics.memory_usage, id: 'memory', unit: ' MiB' },
                { name: 'Network Usage', value: metrics.network_usage, id: 'network', unit: ' kbit/s' }
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
        
        // Choose color based on value
        let color;
        if (safeValue > 80) {
            color = 'rgba(255, 99, 132, 0.8)'; // Red for high
        } else if (safeValue > 60) {
            color = 'rgba(255, 205, 86, 0.8)'; // Yellow for medium
        } else {
            color = 'rgba(75, 192, 192, 0.8)'; // Green for low
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
                maintainAspectRatio: true
            }
        });
    }
});
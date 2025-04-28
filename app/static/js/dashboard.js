document.addEventListener('DOMContentLoaded', function () {
    // set up auto refresh every 10 minutes (600000 ms)
    setInterval(refreshDashboard, 600000)

    // display last updated time
    updateLastUpdatedTime()

    var pieCtx = document.getElementById('pieChart').getContext('2d');
    var barCtx = document.getElementById('barChart').getContext('2d');
    var histCtx = document.getElementById('histogramChart').getContext('2d');
    var lineCtx = document.getElementById('lineChart').getContext('2d');

    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Electronics', 'Clothing', 'Grocery', 'Home Decor'],
            datasets: [{
                data: [30, 25, 20, 25],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4CAF50']
            }]
        }
    });

    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                label: 'Revenue ($)',
                data: [5000, 7000, 8000, 6000, 9000],
                backgroundColor: '#36A2EB'
            }]
        }
    });

    new Chart(histCtx, {
        type: 'bar',
        data: {
            labels: ['0-10', '10-20', '20-30', '30-40', '40+'],
            datasets: [{
                label: 'Orders',
                data: [15, 25, 30, 20, 10],
                backgroundColor: '#FFCE56'
            }]
        }
    });

    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                label: 'Customers',
                data: [100, 200, 300, 400, 500],
                borderColor: '#FF6384',
                fill: false
            }]
        }
    });
});

function refreshDashboard() {
    // refresh the page
    window.location.reload();
}

function updateLastUpdatedTime() {
    const now = new Date();
    document.getElementById('update-item').textContent = now.toLocaleTimeString();
}
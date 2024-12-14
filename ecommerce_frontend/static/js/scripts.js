// Reusable function to render a chart
function renderChart(chartId, chartType, labels, data, options = {}) {
    const ctx = document.getElementById(chartId).getContext("2d");
    new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: options.label || "",
                data: data,
                backgroundColor: options.backgroundColor || [],
                borderColor: options.borderColor || "",
                fill: options.fill || false,
            }]
        },
        options: options.chartOptions || {},
    });
}

// Main script
document.addEventListener("DOMContentLoaded", function () {
    const currentFeature = document.body.getAttribute("data-feature");

    fetch("/api/system_metrics")
        .then(response => response.json())
        .then(data => {
            if (currentFeature === "scalability") {
                renderChart("scalabilityChart", "bar", ["Active Nodes", "Total Requests"], [data.scalability.active_nodes, data.scalability.total_requests], { backgroundColor: ["#4caf50", "#2196f3"] });
            } else if (currentFeature === "fault-tolerance") {
                renderChart("faultChart", "pie", ["Failed Nodes", "Recovered Nodes"], [data.fault_tolerance.failed_nodes, data.fault_tolerance.recovered_nodes], { backgroundColor: ["#f44336", "#8bc34a"] });
            } else if (currentFeature === "security") {
                renderChart("securityChart", "doughnut", ["Secure Requests", "Total Requests"], [data.security.secure_requests, data.security.total_requests], { backgroundColor: ["#009688", "#ffc107"] });
            } else if (currentFeature === "load-balancing") {
                renderChart("loadChart", "line", ["Server 1", "Server 2", "Server 3"], [data.load_balancing.server_1, data.load_balancing.server_2, data.load_balancing.server_3], { borderColor: "#3f51b5", fill: false });
            }
        });
});

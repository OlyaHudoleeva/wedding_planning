function calculateCompletedPercentage(completedTasks = 0, totalTasks = 100) {
        const result = completedTasks / totalTasks * 100;

        const progressBar = document.getElementById("progress-bar");
        progressBar.style.width = "" + result + "%";
}
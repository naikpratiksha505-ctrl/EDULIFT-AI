/**
 * EduLift AI - Dashboard Frontend Scripts
 * Handles Chart.js visualization initialization, search filtering, and UI helpers.
 */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Auto-fill Demo Credentials on Login Page
  const demoStudentBtn = document.getElementById("fill-student-demo");
  const demoFacultyBtn = document.getElementById("fill-faculty-demo");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");

  if (demoStudentBtn && usernameInput && passwordInput) {
    demoStudentBtn.addEventListener("click", function () {
      usernameInput.value = "student_demo";
      passwordInput.value = "Password123!";
    });
  }

  if (demoFacultyBtn && usernameInput && passwordInput) {
    demoFacultyBtn.addEventListener("click", function () {
      usernameInput.value = "faculty_demo";
      passwordInput.value = "Password123!";
    });
  }

  // 2. Real-time Student Search Filter (Faculty Dashboard)
  const studentSearchInput = document.getElementById("student-search");
  if (studentSearchInput) {
    studentSearchInput.addEventListener("input", function (e) {
      const term = e.target.value.toLowerCase().trim();
      const rows = document.querySelectorAll("#student-table-body tr");
      rows.forEach(function (row) {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(term) ? "" : "none";
      });
    });
  }

  // 3. Render Student Marks Progress Chart
  const marksChartCanvas = document.getElementById("studentMarksChart");
  if (marksChartCanvas && typeof Chart !== "undefined") {
    const rawData = marksChartCanvas.getAttribute("data-chart-data");
    if (rawData) {
      try {
        const chartData = JSON.parse(rawData);
        const ctx = marksChartCanvas.getContext("2d");
        new Chart(ctx, {
          type: "line",
          data: {
            labels: chartData.labels,
            datasets: [
              {
                label: "Score Percentage (%)",
                data: chartData.scores,
                borderColor: "#0d9488", // Teal Accent
                backgroundColor: "rgba(13, 148, 136, 0.15)",
                fill: true,
                tension: 0.3,
                pointBackgroundColor: "#0f766e",
                pointRadius: 5,
                pointHoverRadius: 7,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                min: 0,
                max: 100,
                title: {
                  display: true,
                  text: "Score (%)",
                  color: "#64748b",
                },
                grid: {
                  color: "#f1f5f9",
                },
              },
              x: {
                grid: {
                  display: false,
                },
              },
            },
            plugins: {
              legend: {
                display: false,
              },
              tooltip: {
                callbacks: {
                  label: function (context) {
                    return `Score: ${context.parsed.y}%`;
                  },
                },
              },
            },
          },
        });
      } catch (err) {
        console.error("Failed to parse or render marks chart data:", err);
      }
    }
  }

  // 4. Render Faculty Cohort Performance Chart
  const facultyChartCanvas = document.getElementById("facultyCohortChart");
  if (facultyChartCanvas && typeof Chart !== "undefined") {
    const rawData = facultyChartCanvas.getAttribute("data-chart-data");
    if (rawData) {
      try {
        const cohortData = JSON.parse(rawData);
        const ctx = facultyChartCanvas.getContext("2d");
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: cohortData.labels,
            datasets: [
              {
                label: "Average Score (%)",
                data: cohortData.averages,
                backgroundColor: "#1e3a8a", // Navy Blue
                borderRadius: 6,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                min: 0,
                max: 100,
                title: {
                  display: true,
                  text: "Cohort Average (%)",
                  color: "#64748b",
                },
                grid: {
                  color: "#f1f5f9",
                },
              },
              x: {
                grid: {
                  display: false,
                },
              },
            },
            plugins: {
              legend: {
                display: false,
              },
            },
          },
        });
      } catch (err) {
        console.error("Failed to render cohort chart:", err);
      }
    }
  }
});

const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://world-cup-ai-predictor.onrender.com/"; // Replace with your actual live URL later

document.addEventListener("DOMContentLoaded", () => {
  const datePicker = document.getElementById("datePicker");

  // Optional: Trigger fetch immediately on page load for the default date
  fetchMatchesByDate(datePicker.value);

  datePicker.addEventListener("change", (e) => {
    fetchMatchesByDate(e.target.value);
  });
});

async function fetchMatchesByDate(date) {
  const container = document.getElementById("matchContainer");
  container.innerHTML = '<p class="placeholder-text">Loading match data...</p>';

  try {
    const response = await fetch(`/matches?date=${date}`);
    if (!response.ok) throw new Error("Network response was not ok");

    const data = await response.json();

    if (data.matches.length === 0) {
      container.innerHTML = `<p class="placeholder-text">No matches scheduled for ${date}.</p>`;
    } else {
      renderMatches(data.matches);
    }
  } catch (error) {
    container.innerHTML = `<p class="placeholder-text" style="color: red;">Error connecting to the database. Is your backend running?</p>`;
    console.error("Fetch error:", error);
  }
}

function renderMatches(matches) {
  const container = document.getElementById("matchContainer");
  container.innerHTML = "";

  matches.forEach((match) => {
    const card = document.createElement("div");
    card.className = "match-card";

    // Create unique IDs for the dynamic elements
    const resultId = `result-${match.team_a.replace(/\s+/g, "-")}-${match.team_b.replace(/\s+/g, "-")}`;

    // NOTE: 'event' is now passed explicitly into predictMatch
    card.innerHTML = `
      <div class="match-teams">${match.team_a} vs ${match.team_b}</div>
      <div class="match-details">
        <p>🕒 ${match.kickoff_et}</p>
        <p>🏟️ ${match.stadium}</p>
      </div>
      <button type="button" class="predict-btn" onclick="predictMatch(event, '${match.team_a}', '${match.team_b}', '${resultId}')">
        Run AI Analysis
      </button>
      <div id="${resultId}" class="prediction-result" style="display:none;">
        <div class="verdict-text"></div>
        <button type="button" class="stats-toggle-btn" onclick="toggleStats('${resultId}')">Show Stats</button>
        <div class="stats-dashboard" style="display:none;"></div>
      </div>
    `;
    container.appendChild(card);
  });
}

async function predictMatch(event, teamA, teamB, resultElementId) {
  event.preventDefault();
  const resDiv = document.getElementById(resultElementId);
  const btn = resDiv.previousElementSibling; // The "Run Analysis" button

  btn.textContent = "Analyzing...";
  btn.disabled = true;

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ team_a: teamA, team_b: teamB }),
    });

    const data = await response.json();

    // Populate the Verdict and the (hidden) Stats
    resDiv.querySelector(".verdict-text").innerHTML =
      `<strong>AI Verdict:</strong> ${data.prediction}`;

    resDiv.querySelector(".stats-dashboard").innerHTML = `
      <div class="stat-box">
        <span class="stat-label">${teamA} Win</span>
        <span class="stat-value">${data.prob_a}%</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">Draw</span>
        <span class="stat-value">${data.prob_draw}%</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">${teamB} Win</span>
        <span class="stat-value">${data.prob_b}%</span>
      </div>
      <div class="stat-box full-width">
        <span class="stat-label">BTTS: ${data.btts}</span>
        <span class="stat-label">Over 2.5 Goals: ${data.over_2_5}</span>
      </div>
    `;

    resDiv.style.display = "block";
    btn.textContent = "Analysis Complete";
  } catch (error) {
    resDiv.innerHTML = `<p style="color: red;">Analysis Failed. Check backend.</p>`;
    resDiv.style.display = "block";
    btn.textContent = "Try Again";
    btn.disabled = false;
  }
}

function toggleStats(resultId) {
  const resDiv = document.getElementById(resultId);
  const statsDiv = resDiv.querySelector(".stats-dashboard");
  const toggleBtn = resDiv.querySelector(".stats-toggle-btn");

  if (statsDiv.style.display === "none") {
    statsDiv.style.display = "grid";
    toggleBtn.textContent = "Hide Stats";
  } else {
    statsDiv.style.display = "none";
    toggleBtn.textContent = "Show Stats";
  }
}

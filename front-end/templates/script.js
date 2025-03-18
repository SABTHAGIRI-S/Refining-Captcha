let text = "";
let events = [];
let currentKeys = {};

const textArea = document.getElementById("textArea");
const calcBtn = document.getElementById("calcBtn");
const resetBtn = document.getElementById("resetBtn");
const resultDiv = document.getElementById("result");

// Update text as the user types
textArea.addEventListener("input", (e) => {
    text = e.target.value;
});

// Capture keydown events (record only the first press per key)
textArea.addEventListener("keydown", (e) => {
    if (currentKeys[e.code] !== undefined) return;
    events.push({
        key: e.key,
        code: e.code,
        downTime: Date.now(),
        upTime: null
    });
    currentKeys[e.code] = events.length - 1;
});

// Capture keyup events and record upTime
textArea.addEventListener("keyup", (e) => {
    const index = currentKeys[e.code];
    if (index !== undefined) {
        events[index].upTime = Date.now();
        delete currentKeys[e.code];
    }
});

// Calculate metrics based on keystroke events
function calculateMetrics() {
    const validEvents = events.filter(ev => ev.upTime !== null);
    if (validEvents.length < 2) return; // Need at least two events

    // 1. Average_Dwell_Time (ms)
    const dwellTimes = validEvents.map(ev => ev.upTime - ev.downTime);
    const avgDwellTime = dwellTimes.reduce((sum, t) => sum + t, 0) / dwellTimes.length;

    // 2. Average_Flight_Time (ms)
    let flightTimes = [];
    for (let i = 0; i < validEvents.length - 1; i++) {
        flightTimes.push(validEvents[i+1].downTime - validEvents[i].upTime);
    }
    const avgFlightTime = flightTimes.reduce((sum, t) => sum + t, 0) / flightTimes.length;

    // 3. Flight_Time_Std_Dev
    const meanFlight = avgFlightTime;
    const variance = flightTimes.reduce((acc, t) => acc + Math.pow(t - meanFlight, 2), 0) / flightTimes.length;
    const flightStdDev = Math.sqrt(variance);

    // 4. Words_Per_Minute (WPM)
    const totalTimeSec = (validEvents[validEvents.length - 1].upTime - validEvents[0].downTime) / 1000;
    const wordCount = text.length / 5;  // Assuming 5 characters per word
    const wpm = totalTimeSec > 0 ? (wordCount * 60) / totalTimeSec : 0;

    // 5. Human_Like_Typing_Score (H-Score)
    const hScore = 1 / (flightStdDev + 1);

    // Prepare metrics object (keys must match what the backend expects)
    const metrics = {
        "Average_Dwell_Time": parseFloat(avgDwellTime.toFixed(2)),
        "Average_Flight_Time": parseFloat(avgFlightTime.toFixed(2)),
        "Flight_Time_Std_Dev": parseFloat(flightStdDev.toFixed(2)),
        "Human_Like_Typing_Score": parseFloat(hScore.toFixed(4)),
        "Words_Per_Minute": parseFloat(wpm.toFixed(2))
    };

    console.log("Calculated Metrics:", metrics);
    sendMetrics(metrics);
}

// Send the metrics to the Flask API
function sendMetrics(metrics) {
    const url = window.location.origin + "/api/predict";
    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(metrics)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            console.error("Error from server:", data.error);
            return;
        }
        console.log("Server Prediction:", data);
        resultDiv.innerHTML = `<p>Prediction: ${data.prediction}<br>
                               Human Probability: ${data.human_probability.toFixed(2)}<br>
                               Bot Probability: ${data.bot_probability.toFixed(2)}</p>`;
    })
    .catch(error => {
        console.error("Error sending metrics:", error);
        resultDiv.innerHTML = `<p>Error sending metrics: ${error.message}</p>`;
    });
}

// Manual calculation button event
calcBtn.addEventListener("click", calculateMetrics);

// Reset button clears text and events
resetBtn.addEventListener("click", () => {
    text = "";
    textArea.value = "";
    events = [];
    resultDiv.innerHTML = "";
});

// Automatically calculate and send metrics every 5 seconds (if text and events exist)
setInterval(() => {
    if (text.length > 0 && events.length > 0) {
        console.log("Auto-sending metrics...");
        calculateMetrics();
    }
}, 5000);

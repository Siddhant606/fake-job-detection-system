const checkBtn = document.getElementById("checkBtn");
const jobInput = document.getElementById("jobInput");
const resultBox = document.getElementById("resultBox");
const predictionText = document.getElementById("prediction");
const confidenceText = document.getElementById("confidence");
const decisionSourceText = document.getElementById("decisionSource");

checkBtn.addEventListener("click", async () => {
    const jobDescription = jobInput.value.trim();

    if (jobDescription.length < 20) {
        alert("Please enter a valid job description.");
        return;
    }

    try {
        const response = await fetch("https://fake-job-detection-system-s8e6.onrender.com/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                job_description: jobDescription
            })
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        resultBox.classList.remove("hidden");

        predictionText.textContent = `Prediction: ${data.prediction}`;
        confidenceText.textContent = `Confidence: ${data.confidence}`;
        decisionSourceText.textContent = `Decision Source: ${data.decision_source}`;

        resultBox.style.borderLeftColor =
            data.prediction === "FAKE" ? "#dc2626" : "#16a34a";

    } catch (error) {
        alert("Unable to connect to backend server.");
        console.error(error);
    }
});

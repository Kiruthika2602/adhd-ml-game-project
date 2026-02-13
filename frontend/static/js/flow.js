// ----------------------------
// GAME DEFINITIONS
// ----------------------------
const steps = [
    {
        title: "Adaptive Pilot",
        rules: `
• Press SPACE only for YELLOW balls
• Ignore GRAY balls
• Speed increases as time goes on
        `,
        game: runAdaptivePilot,
        resultKey: "adaptive_pilot"
    },
    {
        title: "Flash Reaction",
        rules: `
• React quickly when required
• Click ONLY when color appears
• Avoid unnecessary clicks
        `,
        game: runFlashReaction,
        resultKey: "flash_reaction"
    },
    {
        title: "Steady Shield",
        rules: `
• Keep the mouse as steady as possible
• Follow the moving ball
• Sudden movements increase score
        `,
        game: runSteadyShield,
        resultKey: "steady_shield"
    }
];

// ----------------------------
// STATE
// ----------------------------
let currentStep = 0;
let results = {};

// ----------------------------
// DOM ELEMENTS
// ----------------------------
const titleEl = document.getElementById("title");
const rulesEl = document.getElementById("rules");
const playBtn = document.getElementById("playBtn");
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ----------------------------
// LOAD CURRENT STEP
// ----------------------------
function loadStep() {
    const step = steps[currentStep];

    // Reset canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    titleEl.innerText = step.title;
    rulesEl.innerText = step.rules;

    playBtn.disabled = false;
    playBtn.innerText = `Play ${step.title}`;

    playBtn.onclick = () => {
        playBtn.disabled = true;
        rulesEl.innerText = "Game running...";

        step.game((gameResult) => {
            // Save game result
            results[step.resultKey] = gameResult;

            // Show finished message
            rulesEl.innerText = `${step.title} finished ✔`;

            currentStep++;

            setTimeout(() => {
                if (currentStep < steps.length) {
                    loadStep();
                } else {
                    finishAssessment();
                }
            }, 1500);
        });
    };
}

// ----------------------------
// FINAL STEP → BACKEND
// ----------------------------
function finishAssessment() {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    if (!user.age) {
        alert("User data missing. Please restart assessment.");
        location.href = "index.html";
        return;
    }

    const payload = {
        user: {
            Age: parseInt(user.age),
            Gender: user.gender,
            EducationStage: user.edu,
            SleepHours: parseFloat(user.sleep),
            ScreenTime: parseFloat(user.screen),
            Daydream: user.daydream,
            FamilyHistory: user.family
        },
        adaptive_pilot: results.adaptive_pilot || {},
        flash_reaction: results.flash_reaction || {},
        steady_shield: results.steady_shield || {}
    };

    rulesEl.innerText = "Calculating results...";
    playBtn.style.display = "none";

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(res => {
            if (!res.ok) throw new Error("Backend error");
            return res.json();
        })
        .then(data => {
            localStorage.setItem("finalResult", JSON.stringify(data));
            location.href = "result.html";
        })
        .catch(err => {
            console.error(err);
            alert("Prediction failed. Is backend running?");
        });
}

// ----------------------------
// START
// ----------------------------
loadStep();

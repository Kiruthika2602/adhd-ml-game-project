function runAdaptivePilot(done) {
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    let speed = 3;
    let omissions = 0;
    let distractor_errors = 0;
    let trials = 0;
    let active = true;

    function spawnBall() {
        if (trials >= 40) {
            active = false;
            ctx.clearRect(0, 0, 700, 500);
            alert("Adaptive Pilot finished");
            done({ omissions, distractor_errors });
            return;
        }

        trials++;
        let isTarget = Math.random() < 0.25;
        let isDistractor = Math.random() < 0.15;
        let kind = isTarget ? "target" : isDistractor ? "distractor" : "other";

        let y = 0;
        let responded = false;

        function fall() {
            if (!active) return;
            ctx.clearRect(0, 0, 700, 500);
            ctx.fillStyle = kind === "target" ? "yellow" : "gray";
            ctx.beginPath();
            ctx.arc(350, y, 20, 0, Math.PI * 2);
            ctx.fill();

            y += speed;
            if (y < 500) requestAnimationFrame(fall);
            else {
                if (kind === "target" && !responded) omissions++;
                spawnBall();
            }
        }

        document.onkeydown = e => {
            if (e.code === "Space" && !responded) {
                responded = true;
                if (kind === "distractor") distractor_errors++;
                speed *= 1.05;
            }
        };

        fall();
    }

    spawnBall();
}

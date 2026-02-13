function runSteadyShield(done) {
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    let x = 350, y = 250;
    let vx = 4, vy = 4;
    let jitter = 0;
    let start = Date.now();

    canvas.onmousemove = e => {
        if (Math.abs(e.movementX) > 15 || Math.abs(e.movementY) > 15) {
            jitter++;
        }
    };

    function loop() {
        ctx.fillStyle = "#0a0a2a";
        ctx.fillRect(0, 0, 700, 500);

        x += vx; y += vy;
        if (x < 15 || x > 685) vx *= -1;
        if (y < 15 || y > 485) vy *= -1;

        ctx.fillStyle = "#00ffc8";
        ctx.beginPath();
        ctx.arc(x, y, 15, 0, Math.PI * 2);
        ctx.fill();

        if (Date.now() - start < 15000) {
            requestAnimationFrame(loop);
        } else {
            canvas.onmousemove = null;
            alert("Steady Shield finished");
            done({
                jitter_events: jitter,
                restlessness_events: Math.floor(jitter / 2)
            });
        }
    }

    loop();
}

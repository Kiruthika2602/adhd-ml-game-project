function runFlashReaction(done) {
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    let commission_errors = 0;
    let premature_clicks = 0;
    let trials = 0;

    function nextTrial() {
        if (trials >= 30) {
            ctx.clearRect(0, 0, 700, 500);
            alert("Flash Reaction finished");
            done({ commission_errors, premature_clicks });
            return;
        }

        trials++;
        let isGo = Math.random() < 0.7;
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, 700, 500);

        let waitTime = 500 + Math.random() * 1000;
        let clicked = false;

        const prematureHandler = () => premature_clicks++;
        canvas.onclick = prematureHandler;

        setTimeout(() => {
            canvas.onclick = null;
            ctx.fillStyle = isGo ? "green" : "red";
            ctx.fillRect(0, 0, 700, 500);

            const clickHandler = () => {
                clicked = true;
                if (!isGo) commission_errors++;
            };
            canvas.onclick = clickHandler;

            setTimeout(() => {
                canvas.onclick = null;
                nextTrial();
            }, 600);
        }, waitTime);
    }

    nextTrial();
}

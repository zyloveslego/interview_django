let timerRunning = false;
let startTime = 0;
let interval;

const timerElement = document.getElementById('timer');

recordButton.addEventListener('click', () => {
    timerRunning = true;
    startTime = Date.now() - (startTime || 0);
    interval = setInterval(updateTimer, 1000);
});

stopButton.addEventListener('click', () => {
    timerRunning = false;
    clearInterval(interval);
    timerElement.textContent = '00:00';
    startTime = 0;
});

function updateTimer() {
    const currentTime = Date.now() - startTime;
    const minutes = Math.floor(currentTime / 60000);
    const seconds = Math.floor((currentTime % 60000) / 1000);

    const formattedMinutes = String(minutes).padStart(2, '0');
    const formattedSeconds = String(seconds).padStart(2, '0');

    timerElement.textContent = `${formattedMinutes}:${formattedSeconds}`;
}
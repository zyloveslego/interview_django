const next_link = document.getElementById("nextQuestion");
const currentURL = window.location.href;
// console.log("Current URL: " + currentURL);

const regex = /question_index(\d+)/;
const match = currentURL.match(regex);

if (match) {
    const firstNumber = match[1];
    // window.location.href = currentURL.replace(regex, "question_index=" + (parseInt(firstNumber, 10) + 1));
    next_link.href = currentURL.replace(regex, "question_index" + (parseInt(firstNumber, 10) + 1));
} else {
    console.log("no question_index match");
}




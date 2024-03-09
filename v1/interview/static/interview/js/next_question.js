const next_link = document.getElementById("nextQuestion");
const back_link = document.getElementById("nextQuestion-back");

const currentURL = window.location.href;
// console.log("Current URL: " + currentURL);

const regex = /question_index(\d+)/;
const match = currentURL.match(regex);

if (match) {
    const firstNumber = match[1];
    // window.location.href = currentURL.replace(regex, "question_index=" + (parseInt(firstNumber, 10) + 1));
    next_link.href = currentURL.replace(regex, "question_index" + (parseInt(firstNumber, 10) + 1));
    if ((parseInt(firstNumber, 10) - 1) > 0){
        back_link.href = currentURL.replace(regex, "question_index" + (parseInt(firstNumber, 10) - 1));
        back_link.style.display = 'block';
    }else {
        back_link.style.display = 'none';
    }

} else {
    console.log("no question_index match");
}




//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

let gumStream; 						//stream from getUserMedia()
let rec; 							//Recorder.js object
let input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext; //audio context to help us record

const recordButton = document.getElementById("recordButton");
const stopButton = document.getElementById("stopButton");
//var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
//pauseButton.addEventListener("click", pauseRecording);

//hide AAR contents
//AAR.style.display='none';

function startRecording() {
    console.log("recordButton clicked");

    /*
        Simple constraints object, for more advanced audio features see
        https://addpipe.com/blog/audio-constraints-getusermedia/
    */

    const constraints = {audio: true, video: false};

    /*
       Disable the record button until we get a success or fail from getUserMedia()
   */

    recordButton.disabled = true;
    stopButton.disabled = false;
    //pauseButton.disabled = false

    /*
        We're using the standard promise based getUserMedia()
        https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
            create an audio context after getUserMedia is called
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device

        */
        audioContext = new AudioContext();

        //update the Instruction For Recording
        document.getElementById("instructionForRecording").innerHTML = "Recording...";

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /*
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input, {numChannels: 1});

        //start the recording process
        rec.record();

        console.log("Recording started");

    }).catch(function (err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
        //pauseButton.disabled = true
    });
}

/*function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
    //update the Instruction For Recording 
		document.getElementById("instructionForRecording").innerHTML="Take a breathe...Click 'Resume' when you are ready."

	}else{
		//resume
		rec.record()
		pauseButton.innerHTML="Pause";

    //update the Instruction For Recording 
		document.getElementById("instructionForRecording").innerHTML="Recording..."

	}
}*/

function stopRecording() {
    console.log("stopButton clicked");

//update the Instruction For Recording 
    document.getElementById("instructionForRecording").innerHTML = `Great! Your answer is recorded.<br> Don't forget to submit your answer.`;

//show Your Answer 
    document.getElementById("yourAnswer").innerHTML = "Your Answer:";

    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = true;
    //pauseButton.disabled = true;

    //reset button just in case the recording is stopped while paused
    //pauseButton.innerHTML="Pause";

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
}


var au = document.createElement('audio');
var li = document.createElement('li');
var link = document.createElement('a');
var restart = document.createElement('button');
var submit = document.createElement('button');
restart.classList.add('restart-button');
submit.classList.add('submit-button');

function createDownloadLink(blob) {
    li.style.display = 'block';
    au.style.display = 'block';
    yourAnswer.style.display = 'block';

    var url = URL.createObjectURL(blob);

    //name of .wav file to use during upload and download (without extendion)
    var filename = new Date().toISOString();

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;

    //save to disk link
    link.href = url;
    link.download = filename + ".wav"; //download forces the browser to donwload the file using the  filename
    link.innerHTML = "Save to disk";

    //add the new audio element to li
    showAudio.appendChild(au);

    //add the filename to the li
    //li.appendChild(document.createTextNode(filename+".wav "))

    //add the save to disk link to li
    //li.appendChild(link);

    //my code of adding 'Restart Button'

    restart.innerHTML = "Restart";
    restart.href = "#";
    li.appendChild(restart);

    // submit Answer
    // submit.href = "#";
    submit.innerHTML = "Submit";
    submit.addEventListener("click", function (event) {
        const xhr = new XMLHttpRequest();

        restart.style.display = 'none';
        submit.disabled = true;

        // loading pic show
        document.getElementById("spinner").style.display = 'block';
        document.getElementById("questionBox").style.display = 'none';

        xhr.onload = function (e) {
            if (this.readyState === 4) {
                console.log("Server returned: ", e.target.responseText);
                const response = JSON.parse(this.responseText);
                document.getElementById("my_answer").innerText = response.voice_text;
                document.getElementById("my_assessment").innerText = response.my_access;

                // loading pic hidden
                document.getElementById("spinner").style.display = 'none';

                document.getElementById("questionBox").style.display = 'block';

                sideNavContainer.style.display = 'block';

                AAR.style.display = 'block';
                // alert("Your answer is submitted!");
                document.getElementById("assessment").scrollIntoView({behavior: 'smooth'});
            }
        };
        const fd = new FormData();
        fd.append("audio_data", blob, filename);

        const question_text = document.getElementById("question_text").innerText;
        fd.append("question_text", question_text);

        console.log(upload_url)
        xhr.open("POST", upload_url, true);
        xhr.send(fd);
    })
    li.appendChild(document.createTextNode(" "))//add a space in between
    li.appendChild(submit)//add the upload link to li


    //add the li element to the ol
    recordingsList.appendChild(li);
}


restart.addEventListener("click", function (event) {
    const confirmed = confirm("Are you sure you want to continue? You will lose everything you just recorded.");
    if (confirmed) {
        recordButton.disabled = false;
        //pauseButton.disabled = true;
        stopButton.disabled = true;
        li.style.display = 'none';
        au.style.display = 'none';
        yourAnswer.style.display = 'none';
        document.getElementById("instructionForRecording").innerHTML = "Once ready, click the ‘Record’ button to start recording."
    }

});


// submit.addEventListener("click", function (event) {
//     restart.style.display = 'none';
//     submit.disabled = true;
//     AAR.style.display = 'block';
//     alert("Your answer is submitted!");
//     document.getElementById("assessment").scrollIntoView({behavior: 'smooth'});
// });
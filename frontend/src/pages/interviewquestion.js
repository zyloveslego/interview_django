import React, { useState, useEffect } from 'react';
import { useTheme, styled, Typography, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel, MenuItem, InputLabel, Select, Paper } from '@mui/material/';
import './interviewquestion.css';
import Nav from '../components/nav';
import RecordButton from '../images/RecordButton.svg';
import StopButton from '../images/StopButton.svg';

function InterviewQuestion() {

    const CustomizedSideBarMenuItem = styled(Button)`
color: #fff;
font-size:0.95rem; 
padding-right:2%;
padding-left:2%;
padding-top:0.5rem;
padding-bottom:0.6rem;
display: block;
`;

    const MainContentPaper = styled(Paper)`
padding: 3%;
width: 65%;
text-align: left;
min-height: 420px;
margin-bottom: 2rem;
position: relative;
top: 30px;
`;

    useEffect(() => {
        const scriptRecorder = document.createElement('script');
        const scriptRecorderApp = document.createElement('script');
        const scriptTimer = document.createElement('script');

        scriptRecorder.src = "../js/recorder.js";
        scriptRecorder.async = true;

        scriptRecorderApp.src = "../js/recorderapp.js";
        scriptRecorderApp.async = true;

        scriptRecorderApp.src = "../js/timer.js";
        scriptRecorderApp.async = true;

        document.body.appendChild(scriptRecorder);
        document.body.appendChild(scriptRecorderApp);
        document.body.appendChild(scriptTimer);

        return () => {
            document.body.removeChild(scriptRecorder);
            document.body.removeChild(scriptRecorderApp);
            document.body.removeChild(scriptTimer);
        }
    }, []);

    return (
        <div id="main">
            <Nav />
            <div id="sideNavContainer">
                <Paper elevation={3} sx={{
                    padding: '3%',
                    width: '14%',
                    textAlign: 'center',
                    backgroundColor: 'rgba(126, 95, 80, 0.93)',
                    height: '100%',
                    position: 'fixed',
                    zIndex: '1',
                    top: '0',
                    left: '0',
                    paddingTop: '150px'
                }}>
                    <CustomizedSideBarMenuItem>Questions</CustomizedSideBarMenuItem>
                    <CustomizedSideBarMenuItem>Your Answer</CustomizedSideBarMenuItem>
                    <CustomizedSideBarMenuItem>Vocal Presence</CustomizedSideBarMenuItem>
                    <CustomizedSideBarMenuItem>Assessment</CustomizedSideBarMenuItem>
                    <CustomizedSideBarMenuItem>Revised Answer</CustomizedSideBarMenuItem>
                </Paper>
            </div>

            <div id="mainContent">
                <MainContentPaper elevation={3}>
                    <div id="questionNumber">
                        <div className="theBrownVerticalDecoBar">
                            <p>Interview Practice<br></br>Question 1/5
                            </p>
                        </div>
                        <Typography variant='h5'>Tell me a time you need to meet a tight deadline, but you have multiple other tasks on your table.</Typography>
                    </div>
                    <div id="recorder">
                        <div id="allRecorderButtons">
                            <Button id="recordButton" className="button-1">
                                <img src={RecordButton} alt="Record Button"
                                    className="svgRecorderButton" />
                            </Button>

                            <Button id="stopButton" className="button-1">
                                <img src={StopButton} alt="Stop Button"
                                    className="svgRecorderButton" />
                            </Button>

                            <div id="timer">00:00</div>
                            <script src="./js/timer.js"></script>

                            <div id="instructionForRecording">Once ready, click the ‘Record’ button to start
                                recording.
                            </div>
                        </div>

                        <br></br>
                        <strong>
                            <div id="yourAnswer"></div>
                        </strong>
                        <div id="showAudio"></div>
                        <ol id="recordingsList"></ol>
                        {/*inserting these scripts at the end to be able to use all the elements in the DOM */}
                        <script src="./js/recorder.js"></script>
                        <script src="./js/recorderapp.js"></script>
                    </div>

                </MainContentPaper>

                <div id="AAR">
                    <div id="answerTranscript" class="content-section">
                        <MainContentPaper elevation={3}>
                            <div class="theBrownVerticalDecoBar">
                                <h3>Transcript of Your Answer</h3>
                            </div>
                            <p id="my_answer">I can think of a time at my old job when I had to take the lead in a tricky
                                situation. We had this project where we had to launch a new product, and I was the project
                                manager.

                                <br></br><br></br>The catch was, we had a bunch of people with different skills and personalities on
                                the team. So, I had to step up and make things work:
                                <br></br><br></br>Set the Stage: I kicked things off with a team meeting, laying out what needed to be
                                done, who was responsible for what, and the tight timeline we had.
                                <br></br><br></br>Keep the Chat Flowing: I encouraged everyone to speak their minds and made sure
                                everyone felt heard. No idea was too small or too crazy.
                                <br></br><br></br>Deal with Drama: Of course, there were some disagreements. I jumped in to sort out
                                conflicts and find common ground among team members.
                                <br></br><br></br>In the end, we launched that new product right on schedule and didn't blow our
                                budget. This experience taught me that good leadership makes all the difference in getting a
                                project done well, even with a diverse team.
                            </p>
                        </MainContentPaper>
                    </div>

                    <div id="vocalPresence" class="content-section">
                        <MainContentPaper elevation={3}>
                            <div class="theBrownVerticalDecoBar">
                                <h3>Vocal Presence</h3>
                            </div>
                            <p id="my_vocalPresence"><span>Volume: 4/5</span> - A higher, but still moderate, vocal level projects energy and engagement that captures attention. While the interviewee's current volume effectively conveys ideas, a bolder voice could lend additional authoritativeness and impact to the well-formulated responses.
                                <br></br><br></br><span>Speed: 5/5</span> - The interviewee exhibits an optimal cadence and pacing in their responses. Their rate of speech is measured and appropriate, facilitating easy comprehension.
                                <br></br><br></br><span>Tone: 3/5</span> - While conveying ideas clearly, the interviewee's vocal tone could reveal greater enthusiasm through expanded expressiveness. Adopting a wider vocal range and melodic modulation would further showcase the candidate's innate passion and engagement.
                                <br></br><br></br><span>Precision of Language: 4/5</span> - The interviewee's consistently succinct, filler-free responses demonstrate exemplary preparation and command of language. Their judicious word selection reveals a keen understanding of the power of conciseness to convey maximum meaning.
                            </p>
                        </MainContentPaper>
                    </div>

                    <div id="assessment" class="content-section">
                        <MainContentPaper elevation={3}>
                            <div class="theBrownVerticalDecoBar">
                                <h3>Assessment</h3>
                            </div>
                            <p id="my_assessment">
                                <span>1. Relevance: 9/10</span> - The candidate’s response directly addresses the
                                interviewer’s question, describing a specific disagreement with a colleague and how it was
                                resolved.
                                <br></br><br></br><span>2. Specificity: 8/10</span> - The candidate provides sufficient details to
                                provide context for the disagreement, such as the different priorities each person had and
                                the compromise that was ultimately reached. However, there could have been more specific
                                examples of how the disagreement played out.
                                <br></br><br></br><span>3. Actions: 8/10</span> - The candidate articulates the steps they took to
                                address the situation, such as having an open debate and reaching a compromise. However, it
                                could have been clearer what specific actions the candidate took to contribute to the
                                resolution.
                                <br></br><br></br><span>4. Results and Impact: 8/10</span> - The candidate describes the positive
                                outcome of the disagreement, such as the compromise that was reached. However, there could
                                have been more discussion of the impact of the compromise and how it improved the work.
                                <br></br><br></br><span>5. Learning: 6/10</span> - While the candidate does not mention any major
                                mistakes or failures, they do not discuss any significant lessons learned from the
                                disagreement either.
                                <br></br><br></br><span>6. Clarity: 9/10</span> - The candidate's answer is easy to understand and
                                follow. The language used is clear and concise, and the response is well-structured.
                                <br></br><br></br><span>7. Soft skills: 9/10</span> - The candidate demonstrates several key soft
                                skills, such as communication, problem-solving, and teamwork, in their description of how
                                they resolved the disagreement.

                                <br></br><br></br><span>Overall</span> - I would rate the answer a 8/10. The response provides a clear
                                and relevant example of a disagreement with a colleague and the steps taken to resolve it.
                                However, there could have been more specific examples and discussion of the impact of the
                                compromise, as well as any lessons learned from the situation. The candidate does, however,
                                demonstrate several key soft skills, such as communication, problem-solving, and teamwork,
                                making it a strong response overall.

                            </p>
                        </MainContentPaper>
                    </div>

                    <div id="revisedAnswer" class="content-section">
                        <MainContentPaper elevation={3}>
                            <div class="theBrownVerticalDecoBar">
                                <h3>Revised Answer</h3>
                            </div>
                            <p id="my_revise">One of the most challenging aspects of this project was the team dynamics. We
                                had a diverse group of individuals with varying levels of expertise and different working
                                styles. As the project manager, it was my responsibility to ensure that everyone was aligned
                                with the project's objectives and working cohesively toward the common goal.
                                <br></br><br></br>Here's how I demonstrated leadership skills in this situation:
                                <br></br><br></br>Setting Clear Goals and Expectations: I started by holding a team meeting to outline
                                our project's objectives, scope, and timeline. I made sure everyone understood their roles
                                and responsibilities, emphasizing the importance of their contributions to the project's
                                success.
                                <br></br><br></br>Effective Communication: Throughout the project, I maintained open and transparent
                                communication channels. I encouraged team members to voice their ideas, concerns, and
                                questions. By fostering an environment of trust and open communication, I ensured that
                                everyone felt heard and valued.
                                <br></br><br></br>Conflict Resolution: As expected in any diverse team, conflicts arose. I addressed
                                conflicts promptly, facilitating productive discussions and finding solutions that were
                                acceptable to all parties involved. This helped maintain a positive working atmosphere.
                                <br></br><br></br>In the end, we successfully launched the new product on time and within budget. The
                                project's success was not only a testament to our collective efforts but also a reflection
                                of my ability to lead, inspire, and navigate a diverse team toward a common goal.
                            </p>
                        </MainContentPaper>
                    </div>
                </div>
            </div>
        </div >

    )
}

export default InterviewQuestion;
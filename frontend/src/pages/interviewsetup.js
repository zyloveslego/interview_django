import React, { useState } from 'react';
import './setup.css';
import Nav from '../components/nav';
import { getQuestions } from '../setup';
import { useTheme, styled, Typography, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel, MenuItem, InputLabel, Select, Paper } from '@mui/material/';
import { Link } from 'react-router-dom';

function Setup() {

    const theme = useTheme();
    console.log(theme);

    const [role, setRole] = useState("");
    const [yearsOfExperience, setYearsOfExperience] = useState("");
    const [numOfQuestions, setNumOfQuestions] = useState(0);

    const handleSubmit = async () => {
        const questions = await getQuestions({ role, yearsOfExperience, numOfQuestions });
    }

    return (
        <div className="App">
            <header className="App-header">


                <Paper elevation={3} sx={{ padding: '3%', width: '50%', textAlign: 'left' }}>
                    <div className="theBrownVerticalDecoBar">
                        <Typography variant='h5'>Tell us about yourself and customize your mock interview experience.</Typography>
                    </div>

                    <form>
                        <div className="form-control">
                            <FormControl required>
                                <FormLabel>Choose Your Role</FormLabel>
                                <RadioGroup
                                    name="radio-buttons-group"
                                    value={role}
                                    row={<RadioGroup row />}
                                    onChange={e => setRole(e.target.value)}>
                                    <FormControlLabel value="individual-contributor" control={<Radio />} label="Individual Contributor" />
                                    <FormControlLabel value="manager" control={<Radio />} label="Manager" />
                                </RadioGroup>
                            </FormControl>
                        </div>

                        <FormControl fullWidth>
                            <InputLabel id="demo-simple-select-label">Years of Experience</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={yearsOfExperience}
                                required
                                label="Years of Experience"
                                onChange={e => setYearsOfExperience(e.target.value)}>
                                <MenuItem value="0-1">0-1 year</MenuItem>
                                <MenuItem value="1-3">1-3 years</MenuItem>
                                <MenuItem value="3-5">3-5 years</MenuItem>
                                <MenuItem value="5+">5+ years</MenuItem>
                            </Select>
                        </FormControl>

                        <div className="form-control">
                            <FormControl required>
                                <FormLabel>Number of Questions</FormLabel>
                                <RadioGroup
                                    value={numOfQuestions}
                                    row={<RadioGroup row />}
                                    onChange={e => setNumOfQuestions(e.target.value)}>
                                    <FormControlLabel value={3} control={<Radio />} label="3" />
                                    <FormControlLabel value={5} control={<Radio />} label="5" />
                                    <FormControlLabel value={7} control={<Radio />} label="7" />
                                </RadioGroup>
                            </FormControl>
                        </div>
                        <Button
                            type="submit"
                            color="primary"
                            variant="contained"
                            onSubmit={handleSubmit}>
                            Start Now
                        </Button>
                    </form>
                </Paper>
            </header>
        </div>
    );
}

export default Setup;


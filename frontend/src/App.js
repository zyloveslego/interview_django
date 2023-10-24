import React, { useState } from 'react';
import './App.css';
import Nav from './components/nav';
import Setup from './pages/interviewsetup';
import { getQuestions } from './setup';
import { useTheme, styled, Typography, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel, MenuItem, InputLabel, Select, Paper } from '@mui/material/';
import InterviewQuestion from './pages/interviewquestion';

function App() {



  return (
    <div>
      <InterviewQuestion />
    </div>

  );
}

export default App;


import React, { useState } from 'react';
import './App.css';
import Nav from './components/nav';
import Setup from './pages/interviewsetup';
import { getQuestions } from './setup';
import { useTheme, styled, Typography, Button, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel, MenuItem, InputLabel, Select, Paper } from '@mui/material/';
import InterviewQuestion from './pages/interviewquestion';
import { Route, RouterProvider, createBrowserRouter, createRoutesFromElements } from 'react-router-dom';

const router = createBrowserRouter(createRoutesFromElements(
  <Route path="/" element={<InterviewQuestion />}>
    <Route path="interviewsetup" element={<Setup />} />
    <Route path="interviewquestion" element={<InterviewQuestion />} />
  </Route>
));

function App() {

  return (
    <RouterProvider router={router} />
    // <div>
    //   <Nav />

    // </div>

  );
}

export default App;


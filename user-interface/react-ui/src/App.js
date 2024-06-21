import React from 'react';
import './App.css';
import Container from '@mui/material/Container';
import CarMovement from './components/CarMovement';
import CameraMovement from './components/CameraMovement';
import CameraImagery from './components/CameraImagery';

function App() {
  return (
    <Container maxWidth="sm">
      <h1>Remote Controlled Car</h1>
      <CarMovement />
      <CameraMovement />
      <CameraImagery />
    </Container>
  );
}

export default App;

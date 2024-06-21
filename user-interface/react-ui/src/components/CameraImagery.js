import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import Box from '@mui/material/Box';
import settings from '../settings/settings.json';

const CameraImagery = () => {
  const [socket, setSocket] = useState(null);
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    const newSocket = io(settings.api.url);
    setSocket(newSocket);
    newSocket.on('camera-imagery', (frame) => {
      setImageData(frame);
    });
    return () => newSocket.close();
  }, [setSocket]);

  return (
    <Box>
      {imageData && (
        <img
          style={{ width: '80%', height: 'auto' }}
          src={`data:image/jpeg;base64,${imageData}`}
          alt="Thermal Imagery"
        />
      )}
    </Box>
  );
};

export default CameraImagery;

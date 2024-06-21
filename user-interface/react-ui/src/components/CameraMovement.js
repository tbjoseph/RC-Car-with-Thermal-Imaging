import React, { useEffect, useState, useRef, useCallback } from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import { io } from 'socket.io-client';
import settings from '../settings/settings.json';

const CameraMovement = () => {
  const [socket, setSocket] = useState(null);
  const socketRef = useRef(socket);
  const processingKey = useRef(false);

  const sendCommand = useCallback((direction) => {
    if (socketRef.current) {
      socketRef.current.emit('car-movement', direction);
    }
  }, []);

  const handleKeyDown = useCallback(
    (e) => {
      const keyToDirection = {
        j: 'left',
        k: 'right',
      };

      const direction = keyToDirection(e.key.toLowerCase());

      if (direction && !processingKey.current) {
        processingKey.current = true;
        sendCommand(direction);
      }
    },
    [sendCommand],
  );

  const handleKeyUp = useCallback(
    (e) => {
      const validKeys = ['j', 'k'];

      if (validKeys.includes(e.key.toLowerCase()) && processingKey.current) {
        processingKey.current = false;
        sendCommand('stop');
      }
    },
    [sendCommand],
  );

  useEffect(() => {
    const newSocket = io(settings.api.url);
    setSocket(newSocket);
    socketRef.current = newSocket;

    return () => {
      newSocket.disconnect();
    };
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [handleKeyDown, handleKeyUp]);

  return (
    <Grid container spacing={2} alignItems="center" justifyContent="center">
      <Grid item>
        <Button
          onMouseDown={() => sendCommand('left')}
          onMouseUp={() => sendCommand('stop')}
        >
          Rotate left (J)
        </Button>
      </Grid>
      <Grid item>
        <Button
          onMouseDown={() => sendCommand('right')}
          onMouseUp={() => sendCommand('stop')}
        >
          Rotate right (K)
        </Button>
      </Grid>
    </Grid>
  );
};

export default CameraMovement;

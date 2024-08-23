## Overview
This repository houses the project for a remote-controlled car equipped with thermal imaging capabilities, designed to navigate and analyze environments where human access is restricted or dangerous. This RC Car project combines hardware manipulation with real-time data streaming to provide a comprehensive view of the surroundings using thermal imaging.
This project serves as a sophisticated tool for remote environmental assessment, ideal for applications in disaster recovery, military reconnaissance, and industrial inspection where thermal imaging provides critical insights not visible to the naked eye.

## Features
* Mobile Platform with Thermal Imaging: Equipped with an infrared camera mounted on a rotating gimbal, providing 360-degree thermal imaging capabilities.
* Remote Operation: Fully controllable via a user interface, allowing for remote navigation and camera manipulation.
* Real-Time Data Streaming: Utilizes websockets for real-time communication and streaming of thermal imagery to the user interface.
* Enhanced Navigation: The car chassis includes four DC motors controlled via dual L298N motor drivers for improved handling and mobility.
* Precision Control: Features a stepper motor for precise gimbal movements, managed by an A4988 stepper motor driver.
* Robust System Design: Incorporates a Raspberry Pi interfaced with motor drivers and an infrared camera using I2C, ensuring reliable data handling and device control.
* Intuitive User Interface: Developed with React for the frontend and Flask for the backend, facilitating easy control and monitoring of the RC Car.

## System Design
* Motor Control: Four wheel motors connected through L298N motor drivers to the Raspberry Pi, ensuring safe operation by providing necessary current and voltage protection.
* Camera Gimbal: Infrared camera mounted on a stepper motor-controlled gimbal for comprehensive environmental imaging.
* Data Handling: MLX90640 infrared camera with a 32x24 pixel array sends imaging data to the Raspberry Pi via I2C.
* User Interaction: Websockets-based UI allows for responsive command processing and streaming of thermal imaging data, hosted on a Flask server running on the Raspberry Pi.
* Real-Time Imaging: Continuous thermal data stream via websockets, displayed dynamically in the React-based frontend.

## Outcomes
* Responsive Control: The car is controllable in real-time through websockets, ensuring immediate responsiveness to user commands.
* High Framerate Imaging: Multithreading implementation allows for a higher-than-expected framerate from the thermal camera.
* Mobility Adjustments: The car's speed is moderated by the weight of the portable battery, optimizing for power over speed to maintain system stability and imaging quality.

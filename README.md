# DJI Tello Drone Project

Reference: https://www.youtube.com/watch?v=LmEcyQnfpDA

## Python Packages

- djitellopy
- pygame
- cv2
- numpy

## Filelist

1. Basic Movement

Simple test to check operation. Take off wait and land

2. Image Capture

Test to check if the drone is able to capture images using its camera

3. Keyboard control

pressing keys on the computer keyboard to make the drone move

4. Surveillance

Using Image Capture & Keyboard Control to record photo images

5. Mapping

Map your own route on the computer and the drone will follow the directions on the computer (using the up,down,left,right keys)

6. Face Tracking

The drone will track your face and move along a certain distance(too close,move back. too far, move forward.)

7. Line Follower

The drone will follow a line (using a color picker. In my case, white)and change directions as it moves so to complete the course

## Test if python installed

For Python version 3

```bash
python3 -V

python -V # coutd be for version 2 which should not be used
```

## Create python virtual environment for project

Call the virtual environment `dev`

```bash
python3 -m venv dev
```

To activate

```
source dev/bin/activate
```

To deactivate, just type `exit`

## Installing tello library

```
pip3 install djitellopy
```

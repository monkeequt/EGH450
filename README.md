# EGH450 - UAS_FIRE (Group 6)

A team of Group 6 engineers designing an autonomous bushfire detection and extinguishing drone for QUT's EGB349 and EGH450 in 2026. The project covers the planning, design, build and flight testing of UAS_FIRE.

This repository contains the software developed for the QUT EGB349/EGH450 **Bushfire Detection & Extinguishing (UAS_FIRE)** project.

The system autonomously searches an indoor area, detects and localises fire, smoke and ArUco targets, and displays and vocalises mission information to an operator. It drops a fire-extinguishing payload mid-air over each threat, then lands on a designated ArUco marker.

The image dataset used for training can be found here:

https://universe.roboflow.com/egh455-vbb5h/sar-mission-ucsok
---

## System Overview

### UAV Hardware
- Holybro X500 V2 airframe
- Pixhawk 6X autopilot (PX4)
- Raspberry Pi 4B onboard computer / ROS master
- Luxonis OAK-D Pro RGB-D camera
- OptiTrack external localisation (VRPN)
- Dual servo payload deployment system (one fire payload, one smoke payload)

### Ground Control Station
- Raspberry Pi 400
- RViz
- RQT
- QGroundControl
- Manual RC controller (Foxtech DA16s+)
- Distributed ROS and SSH connection to the onboard Raspberry Pi 4B

### Software
- Ubuntu 20.04
- ROS Noetic
- PX4
- MAVROS
- QUTAS ROS packages (SPAR, Breadcrumb, qutas_lab_450, UAVASR emulator)
- DepthAI
- OpenCV
- YOLOv5
- Python 3

---

## Repository Structure

This repository **is** the catkin workspace. On the drone it lives at:

```
~/catkin_ws_G6/
```

Several launch files and scripts use absolute paths under `/home/uavteam6/catkin_ws_G6/`, so keep this location on the Pi.

```
catkin_ws_G6/
├── launch/
│   ├── control.launch          # MAVROS + SPAR flight server (physical UAV)
│   ├── breadcrumb.launch       # A* path planner with O-134 bounds
│   ├── px4_config.yaml         # MAVROS config
│   └── px4_pluginlists.yaml    # MAVROS plugin blacklist
├── config.yaml
├── pi_ip_automatedV2.py        # Sends the Pi's IP address to Discord on boot
├── autofocus_query.py          # Lists the connected OAK-D camera features
└── src/
```

The main packages used by the current system are:

```
src/
├── spar/                       # SPAR flight action server + bfr2 mission guidance node
├── breadcrumb/                 # QUTAS A* path planner (occupancy grid)
├── qutas_lab_450/              # O-134 environment, occupancy grid, VRPN OptiTrack, RQT dashboard
├── depthai_publisher/          # OAK-D Pro camera, fire/smoke YOLO runner, ArUco detector
├── flight_aruco_navigation/    # Camera → world transforms for ArUco and fire/smoke (physical flight)
├── servo_control/              # Payload servo node (GPIO PWM)
├── vocaliser/                  # Text-to-speech for /chatter (espeak)
├── uavasr_emulator/            # QUTAS UAV emulator for simulation
├── uavasr_aruco_navigation/    # Camera → world transforms (emulator version)
├── rqt_generic_hud/            # GCS plugins
├── rqt_mavros_gui/
├── rqt_eyedropper/
└── rqt_quaternion_view/
```

Older and reference packages kept in the workspace:

```
src/aruco_navigation/           # Early TF2 broadcaster experiments
src/drone_servos/               # Earlier version of the servo node
src/egh450_image_processor/     # QUTAS Haar cascade demo
src/egh450_target_solvepnp/     # QUTAS solvePnP demo
src/depthai-ros/                # Luxonis DepthAI ROS driver (upstream)
```

---

## Prerequisites

- Ubuntu 20.04
- ROS Noetic
- Python 3
- PX4
- MAVROS
- QGroundControl
- DepthAI (`python3 -m pip install -U depthai`)
- OpenCV (with `cv2.aruco`)
- `vrpn_client_ros`
- `RPi.GPIO` (Pi 4B, for the servos)
- `python3-espeak` (Pi 400, for the vocaliser)
- tmux
- RViz
- RQT

ROS packages used by the camera nodes:

```bash
sudo apt-get install ros-noetic-compressed-image-transport ros-noetic-camera-info-manager \
  ros-noetic-rqt-image-view ros-noetic-cv-bridge ros-noetic-vision-opencv
```

---

## Hardware Setup

| Item | Part |
|---|---|
| Airframe | Holybro X500 V2 |
| Autopilot | Pixhawk 6X |
| On-board computer | Raspberry Pi 4B |
| Ground control station | Raspberry Pi 400 |
| Camera | Luxonis OAK-D Pro (mounted 0.125 m behind and 0.1 m above the UAV origin) |
| Localisation | OptiTrack, rigid body `uavteam6` |
| Payload | Dual servo release system |
| Manual control | DA16s+ RC transmitter |

| Link | Connection |
|---|---|
| Pi 4B ↔ Pixhawk | `/dev/ttyUSB0` at **921600** baud, MAVLink v2, system ID **6** |
| Pi 4B → servo 1 (fire) | GPIO **12** (BCM), 50 Hz PWM |
| Pi 4B → servo 2 (smoke) | GPIO **13** (BCM), 50 Hz PWM |
| OptiTrack → Pi 4B | VRPN server `10.68.42.85:3883` |

---

## Installation and Workspace Setup

### 1. Clone Repository

Clone the repository onto the Raspberry Pi 4B as the workspace:

```bash
git clone https://github.com/monkeequt/EGH450.git ~/catkin_ws_G6
cd ~/catkin_ws_G6
```

### 2. Build ROS workspace

```bash
cd ~/catkin_ws_G6
catkin_make
source devel/setup.bash
```

Source the workspace in every terminal before running project ROS nodes. You can add it to your `~/.bashrc`:

```bash
echo "source ~/catkin_ws_G6/devel/setup.bash" >> ~/.bashrc
```

### 3. (Optional) IP address on boot

`pi_ip_automatedV2.py` posts the Pi 4B's Wi-Fi IP address to a Discord channel through a webhook. Set `WEBHOOK_URL` in the script, then add it to the crontab:

```bash
crontab -e
# add:
@reboot sleep 60 && /usr/bin/python3 /home/uavteam6/catkin_ws_G6/pi_ip_automatedV2.py
```

---

## Distributed ROS Setup

The Raspberry Pi 4B acts as the ROS master and runs the main UAV software. The Raspberry Pi 400 acts as the Ground Control Station and is used for:

- RViz
- RQT
- telemetry monitoring
- camera viewing
- vocalised alerts
- operator control

Both Raspberry Pis must be connected to the same network.

### 1. Start the Raspberry Pi 4B ROS Master

From the Raspberry Pi 400, SSH into the Raspberry Pi 4B:

```bash
ssh uavteam6@<PI_4B_IP>
```

You can get `<PI_4B_IP>` from the Discord message the Pi sends on boot.

Start ROS core on the Pi 4B (see [Running the Nodes](#running-the-nodes) for the full start-up order):

```bash
roscore
```

### 2. Connect Raspberry Pi 400 to the ROS Master

Open a separate terminal on the Raspberry Pi 400 and run:

```bash
disros <PI_4B_IP>
```

Confirm that the Raspberry Pi 400 can communicate with the ROS master:

```bash
rostopic list
```

If the ROS topics are listed, distributed ROS is working. The Pi 4B is the ROS master; the Pi 400 is used for visualisation and operator tools.

---

## Running the Nodes

Run each command in its own terminal (or tmux pane), in this order. All terminals on the Pi 4B must have the workspace sourced.

### On the Raspberry Pi 4B

```bash
# 1. ROS master
roscore

# 2. MAVROS + SPAR flight server
roslaunch ~/catkin_ws_G6/launch/control.launch

# 3. OptiTrack (VRPN), occupancy grid with obstacle pillars, home frame
roslaunch qutas_lab_450 environment.launch obstacle0_x:=<cell> obstacle0_y:=<cell> obstacle1_x:=<cell> obstacle1_y:=<cell>

# 4. Breadcrumb path planner
roslaunch ~/catkin_ws_G6/launch/breadcrumb.launch

# 5. OAK-D Pro camera + fire/smoke YOLO
rosrun depthai_publisher yolov5_runner_distance_est_v3.py

# 6. ArUco detector
rosrun depthai_publisher aruco_subscriber_pose

# 7. Camera → world transforms for ArUco and fire/smoke
roslaunch flight_aruco_navigation flight_aruco_navigation.launch

# 8. Payload servos
rosrun servo_control actuator_control.py

# 9. Mission guidance (start last)
roslaunch spar_node bfr2.launch landing_aruco_id:=<ID> survey_alt:=<HEIGHT>
```

### On the Raspberry Pi 400 (GCS)

```bash
disros <PI_4B_IP>

# Vocalised alerts (run on the GCS so audio plays from its speaker)
rosrun vocaliser vocaliser.py

# RQT dashboard (battery, flight mode, arming)
roslaunch qutas_lab_450 dashboard.launch

# Camera feed
rqt_image_view

# 3D view
rviz
```

---

## RViz Setup

After running:

```bash
disros <PI_4B_IP>
```

launch RViz from the Raspberry Pi 400:

```bash
rviz
```

Set the **Fixed Frame** to `map` and add these displays:

| Display | Topic | Shows |
|---|---|---|
| TF | — | `map`, `uav`, `camera` and `home` frames |
| Pose | `/mavros/local_position/pose` | UAV position |
| Map | `/grid` | Occupancy grid |
| MarkerArray | `/markers` | Obstacle pillars |
| Path | `/guidance/fullPath` | Planned search pattern |
| Path | `/guidance/pathBreadcrum` | Current Breadcrumb route |
| MarkerArray | `/aruco_detection/world_markers` | Detected ArUco markers with IDs |
| MarkerArray | `/target_detection/world_markers` | Detected fire and smoke |
| MarkerArray | `/guidance/image_targets` | Where each payload was dropped |
| Image | `/depthai_node/detection/compressed` | YOLO annotated camera feed |

Save the configuration with **File → Save Config As** so it can be reloaded with `rviz -d <file>.rviz`.

If RViz opens but some displays are missing, check the current ROS topics using:

```bash
rostopic list
```

and update the affected topic selections if required.

---

## Vision System

The vision system uses the OAK-D Pro camera to run both YOLO fire/smoke detection and ArUco marker detection on board the Raspberry Pi 4B.

The current vision system uses:

- YOLOv5 model `150 epoch Rosbag Bright 2 5 Shave`
- 416x416 camera input
- 20 FPS camera feed
- Fire and smoke detection
- Stereo depth for target distance
- ArUco 5x5 marker detection

The vision system is started with:

```bash
rosrun depthai_publisher yolov5_runner_distance_est_v3.py
rosrun depthai_publisher aruco_subscriber_pose
```

The main camera topics are:

```
/depthai_node/image/compressed
/depthai_node/detection/compressed
/processed_aruco/image/compressed
/depthai_node/camera/camera_info
```

| Topic | Content |
|---|---|
| `/depthai_node/image/compressed` | Raw camera image |
| `/depthai_node/detection/compressed` | YOLO annotated image (fire and smoke) |
| `/processed_aruco/image/compressed` | ArUco annotated image (outline, ID, centre, distance) |

The annotated images can be viewed using:

```bash
rqt_image_view
```

Then select the topic from the list.

### YOLO Target Detection

The YOLO model detects **Fire** and **Smoke** printed targets within the search area.

The model files are stored in:

```
src/depthai_publisher/Models/Best_Shave/
```

The active model is set at the top of:

```
src/depthai_publisher/src/depthai_publisher/yolov5_runner_distance_est_v3.py
```

```python
modelsPath = "/home/uavteam6/catkin_ws_G6/src/depthai_publisher/Models"
modelName  = '150 epoch Rosbag Bright 2 5 Shave'
confJson   = 'best.json'
File_name  = 'Best_Shave'
```

The detection settings come from `Models/Best_Shave/best.json`:

| Setting | Value |
|---|---|
| Model | `150 epoch Rosbag Bright 2 5 Shave.blob` |
| Classes | `Fire`, `Smoke` |
| Input size | 416x416 |
| Confidence threshold | 0.70 |
| IoU threshold | 0.50 |
| Camera FPS | 20 |

For each detection, the runner reads the OAK-D stereo depth around the bounding-box centre (median of a small window). It then uses the camera intrinsics to calculate a camera-relative XYZ position in metres, and publishes it as a `visualization_msgs/Marker` on:

```
/depthai_node/detection/pose
```

`flight_target_navigation.py` transforms each detection into the `map` frame using the OptiTrack-driven `map → uav → camera` TF tree. It publishes the result on:

```
/target_detection/world_pose
/target_detection/world_markers
```

The first time each target type is seen, the vocaliser announces *"Fire detected"* or *"Smoke detected"*.

### ArUco Detection

ArUco markers are logged as points of interest, and one of them is used as the final landing pad.

The detector uses:

```
DICT_5X5_250
```

The detector calculates each marker's pose with `solvePnP` and publishes the ID and camera-relative position on `/aruco_detection/pose`. `flight_aruco_navigation.py` transforms it into the `map` frame and keeps a latched list of every unique marker found:

```
/aruco_detection/pose
/aruco_detection/world_pose
/aruco_detection/world_markers
/aruco_detection/unique_ids
```

Each new marker is announced as *"ArUco marker N detected"*.

The landing marker ID is set when launching the guidance node:

```bash
roslaunch spar_node bfr2.launch landing_aruco_id:=<ID>
```

The detector needs a current OptiTrack pose before it can convert a marker position into world coordinates.

ArUco detection works best when:

- The complete marker is visible
- The image is not affected by motion blur
- The marker border can be clearly seen
- There are no strong reflections on the marker
- The UAV is moving slowly over the marker

---

## Guidance System

The autonomous mission is controlled by the `bfr2` guidance node, which sends goals to the QUTAS **SPAR** flight action server (`spar/flight`).

The guidance node and its configuration are in:

```
src/spar/spar_node/scripts/bfr2            # mission logic + search waypoints
src/spar/spar_node/launch/bfr2.launch      # parameters
```

`bfr2.launch` contains:

- Survey altitude
- Linear and yaw velocities
- Takeoff and landing speeds
- Position and yaw tolerances
- Payload deployment height and hover time
- Target confirmation settings
- Battery threshold and fallback landing position
- Safe flight boundaries
- ROS topic names

`bfr2.launch` also starts `battery_manager.py`. This node republishes `/mavros/battery` (or the emulator battery) on `/uav/battery` for the guidance node.

The mission follows this general sequence:

1. Take off from `[-1, -1]`
2. Fly the lawnmower search waypoints at survey altitude
3. Detect fire or smoke (two or more detections within 0.4 s to confirm)
4. Divert to the target along a Breadcrumb path
5. Descend to 0.5 m above the target and hover for 5 s
6. Deploy the matching payload
7. Return along Breadcrumb to the point where the search was interrupted
8. Complete the remaining waypoints
9. Fly to the landing ArUco along Breadcrumb
10. Descend to 0.5 m, hover for 5 s, then land

If a second target is seen during a diversion, it is queued and handled after the UAV returns to the survey.

If a full search pass finishes without both payloads deployed, or without the landing ArUco found, the search pattern is **repeated**. Once at least one full pass is complete, both payloads are deployed and the landing marker is known, the UAV returns to land.

The guidance node waits for the SPAR flight server and the Breadcrumb service. The SPAR flight server becomes available after:

- MAVROS is connected
- A valid UAV pose is available
- The UAV is armed
- OFFBOARD mode is selected

Once these conditions are met, the autonomous mission begins.

### Search Pattern

The search waypoints are defined in `main()` of:

```
src/spar/spar_node/scripts/bfr2
```

The search is a lawnmower pattern from X = −4.0 to 3.6 m, with passes about 0.6 m apart from Y = −3.25 to 1.75 m. The first waypoint is the take-off point `[-1, -1]`. Every leg between waypoints is planned through Breadcrumb, so the UAV routes around the obstacle pillars.

All waypoint coordinates are relative to the OptiTrack world origin. Before flying in a different area, check:

- The location of the world origin
- The positive X and Y directions
- The flight boundaries (`safeRangeX` 4.4 m, `safeRangeY` 3.3 m, `safeRangeZ` 4.0 m)
- The Breadcrumb bounds in `launch/breadcrumb.launch` (X −4.0 to 4.0, Y −3.2 to 2.0, Z 0.5 to 4.0)
- The flight height
- The distance between each search pass
- The fallback landing position

### Obstacles

The two pillar obstacles go into the occupancy grid through `environment.launch`. Their positions are given in **grid cells**, not metres. The grid is 100 × 100 cells at 0.1 m per cell, centred on the world origin, so:

```
cell = (metres × 10) + 50
```

For example, a pillar at X = 1.0 m, Y = −0.5 m is `obstacle0_x:=60 obstacle0_y:=45`.

Check the pillars appear in the right place in RViz (`/grid`) before flying.

---

## Payload Deployment

The payload system uses two servos on the Pi 4B GPIO. Each servo releases one payload.

| Detection | Servo | GPIO (BCM) | Topic |
|---|---|---|---|
| Fire | Servo 1 | 12 | `/actuator_control/servo1` |
| Smoke | Servo 2 | 13 | `/actuator_control/servo2` |

The servo node takes `std_msgs/Bool` messages:

| Message | Duty cycle | Servo position |
|---|---|---|
| `True` | 12.5% | Closed (loads and holds the payload) |
| `False` | 2.5% | Open (releases the payload) |

The payload system is started through:

```bash
rosrun servo_control actuator_control.py
```

To load the payloads before a flight, close both servos manually:

```bash
rostopic pub -1 /actuator_control/servo1 std_msgs/Bool "data: true"
rostopic pub -1 /actuator_control/servo2 std_msgs/Bool "data: true"
```

To test the release:

```bash
rostopic pub -1 /actuator_control/servo1 std_msgs/Bool "data: false"
rostopic pub -1 /actuator_control/servo2 std_msgs/Bool "data: false"
```

During the mission, the guidance node publishes `False` to the matching servo after the 5 s hover. Only one payload of each type can be deployed per mission.

Test the servo and payload system **with the propellers removed** before each assessed flight.

---

## Simulation (UAVASR Emulator)

The mission can be tested without the drone using the QUTAS emulator:

```bash
roscore
roslaunch spar_node spar_uavasr.launch obstacle0_x:=<cell> obstacle0_y:=<cell> obstacle1_x:=<cell> obstacle1_y:=<cell>
roslaunch ~/catkin_ws_G6/launch/breadcrumb.launch
roslaunch spar_node bfr2.launch landing_aruco_id:=<ID>
rviz
```

In the emulator, the battery manager simulates battery discharge. It reaches the threshold after `emulator_time_to_threshold_seconds` (600 s by default), so the low-battery failsafe can be tested.

---

## Important ROS Topics

The main topics used during the mission are:

```
/mavros/state
/mavros/local_position/pose
/mavros/vision_pose/pose
/mavros/battery
/uav/battery

/depthai_node/image/compressed
/depthai_node/detection/compressed
/depthai_node/detection/pose
/depthai_node/camera/camera_info

/processed_aruco/image/compressed
/aruco_detection/pose
/aruco_detection/world_markers
/aruco_detection/unique_ids

/target_detection/world_pose
/target_detection/world_markers

/guidance/fullPath
/guidance/pathBreadcrum
/guidance/image_targets

/actuator_control/servo1
/actuator_control/servo2

/chatter
/grid
```

These topics can be checked using:

```bash
rostopic list
```

---

## Pre-Flight Checks

Before starting a flight, check:

- The UAV battery is charged
- The RC controller is connected
- Manual control has been tested
- The propellers are correctly installed
- Both payloads are loaded and the servos are closed
- The OAK-D Pro is connected
- The Pixhawk is connected to `/dev/ttyUSB0`
- Both Raspberry Pis are connected to the same network
- The Raspberry Pi 4B IP address is known
- OptiTrack is tracking the `uavteam6` rigid body
- MAVROS is connected
- UAV position data is updating
- The obstacle pillars are in the right place on `/grid`
- Camera images are being published
- The YOLO model is running
- ArUco detection is running
- The landing ArUco ID and survey altitude have been set for the day
- The vocaliser is running on the GCS
- RViz is receiving the correct topics
- There is enough storage for rosbag recording
- The flight area is clear

Check MAVROS using:

```bash
rostopic echo /mavros/state
```

Check the local UAV position using:

```bash
rostopic echo /mavros/local_position/pose
```

Check the OptiTrack pose using:

```bash
rostopic echo /mavros/vision_pose/pose
```

The local position and OptiTrack pose should agree. If they don't, the EKF2 estimate is diverging, so do not fly.

Check the battery using:

```bash
rostopic echo /mavros/battery
```

Check the raw camera frame rate using:

```bash
rostopic hz /depthai_node/image/compressed
```

Check the YOLO annotated frame rate using:

```bash
rostopic hz /depthai_node/detection/compressed
```

---

## Running the Mission

Before starting the mission:

- Complete the pre-flight checks
- Start rosbag recording
- Confirm that the flight area is clear
- Confirm the UAV position in RViz
- Confirm that the camera feed is visible
- Confirm that the payloads are installed correctly
- Confirm that the pilot is ready to take manual control

The pilot can then:

1. Arm the UAV
2. Confirm that the UAV remains stable
3. Select OFFBOARD mode
4. Monitor the autonomous mission

Once OFFBOARD mode is selected and the SPAR server is available, the guidance system starts the mission.

During the flight, monitor:

- UAV position
- Battery level
- MAVROS connection
- OptiTrack pose
- Camera frame rate
- YOLO detections
- ArUco detections
- Payload deployment
- Current mission state (guidance terminal)

The RC pilot must stay ready to take manual control for the entire flight.

---

## Recording Flights

Rosbags are used to record flight information and camera images for later testing.

To record all ROS topics:

```bash
rosbag record -a
```

To create a rosbag with the date and time in its name:

```bash
rosbag record -O flight_$(date +%Y%m%d_%H%M%S).bag -a
```

To record only the camera topics:

```bash
rosbag record -O images_$(date +%Y%m%d_%H%M%S).bag /depthai_node/image/compressed /depthai_node/detection/compressed /processed_aruco/image/compressed
```

To extract images from a bag for YOLO training, use:

```
src/depthai_publisher/scripts/bags2images.py
```

Stop the recording using:

```
Ctrl+C
```

Stop the rosbag properly before shutting down the Raspberry Pi so the file isn't corrupted.

---

## Mission Shutdown

After the UAV has landed:

1. Confirm that the UAV is disarmed
2. Stop the rosbag recording
3. Stop the guidance and vision nodes
4. Close RViz and RQT
5. Shut down the onboard Raspberry Pi
6. Disconnect the UAV battery
7. Remove any remaining payloads
8. Save the rosbag and screen recording

The UAV must be disarmed before anybody approaches it.

---

## Common Problems

### No ROS topics on the Raspberry Pi 400

Check:

- Both Raspberry Pis are on the same network
- `disros` was run with the correct IP address
- ROS core is running on the Raspberry Pi 4B

Run:

```bash
rostopic list
```

### MAVROS is not connected

Check:

- The Pixhawk USB/serial connection
- `/dev/ttyUSB0` exists
- The baud rate is set to 921600
- The Pixhawk is powered
- The target system ID is 6

### No OptiTrack position

Check:

- The `uavteam6` rigid body is enabled in Motive
- OptiTrack streaming is running
- The UAV is visible to the OptiTrack cameras
- `environment.launch` is running (VRPN client to `10.68.42.85`)
- `/mavros/vision_pose/pose` is updating

### No camera images

Check:

- The OAK-D Pro USB connection
- The vision terminal for any DepthAI errors
- The model path in `yolov5_runner_distance_est_v3.py`
- No other program is already using the camera (only one node can open the OAK-D at a time)

Run `python3 ~/catkin_ws_G6/autofocus_query.py` to confirm the camera is detected.

### YOLO is running but ArUco is not detecting

Check:

- The complete marker is visible
- The marker is from the 5x5 dictionary
- The marker is large enough in the image
- The landing marker ID is correct
- The image is not blurred
- `aruco_subscriber_pose` is running and `/processed_aruco/image/compressed` is publishing

### Targets are detected but do not appear in the world frame

Check that `flight_aruco_navigation.launch` is running, and that the TF tree is complete:

```bash
rosrun tf view_frames
```

The tree should contain `map → uav → camera`.

### The mission does not begin

Check:

- MAVROS is connected
- A valid UAV pose is available
- The UAV is armed
- OFFBOARD mode is selected
- The `/spar/flight` action server is available
- The `/breadcrumb/request_path` service is available (`rosservice list`)

### A target is detected but the UAV does not divert

Check that detections are arriving:

```bash
rostopic echo /depthai_node/detection/pose
```

Then check the guidance terminal. A target needs at least two detections within 0.4 s to be confirmed. A target that has already received its payload is ignored.

### The payload does not deploy

Check:

```bash
rostopic echo /actuator_control/servo1
rostopic echo /actuator_control/servo2
```

Also check that `actuator_control.py` is running, and check the servo power, GPIO 12/13 connections and payload positions.

### No voice alerts

Check that `vocaliser.py` is running on the GCS and that `/chatter` is publishing:

```bash
rostopic echo /chatter
```

---

## Known Limitations

- ArUco detection becomes less reliable at greater heights
- Fast UAV movement can cause motion blur
- The system requires a valid OptiTrack pose
- The search waypoints are configured for the O-134 assessed flight area
- Obstacle positions must be entered as grid cells, not metres
- The obstacle arguments in `bfr2.launch` are not used by the guidance node; obstacles come only from the occupancy grid
- `bfr2.launch` remaps the guidance pose to `/uavasr/pose` (emulator). For physical flight this needs to be `/mavros/local_position/pose`
- Some launch files and scripts use absolute paths for the `uavteam6` Raspberry Pi
- Camera performance depends on the lighting and USB connection
- Older scripts and model versions remain in the repository for testing and reference

---

## Main Project Packages

**spar**
Provides the SPAR flight motion action server. Also contains the `bfr2` mission guidance node and `battery_manager.py`.

**breadcrumb**
Contains the supplied A* path planner, used with the occupancy grid to route around obstacles.

**qutas_lab_450**
Contains the O-134 environment: occupancy grid, obstacle visualisation, VRPN OptiTrack client and the RQT dashboard.

**depthai_publisher**
Runs the OAK-D Pro camera, the fire/smoke YOLO model with stereo depth, and the ArUco detector. Publishes the raw image, annotated images, detections and camera information.

**flight_aruco_navigation**
Broadcasts the `map → uav → camera` TF tree for physical flight. Transforms ArUco and fire/smoke detections into the world frame and announces each new detection.

**servo_control**
Controls the two payload servos through Pi 4B GPIO.

**vocaliser**
Reads every message on `/chatter` aloud using espeak.

**uavasr_emulator / uavasr_aruco_navigation**
Simulation versions of the UAV and world-transform nodes, used for testing the mission without flying.

---

## Current Demo Configuration

The current assessed flight configuration is:

| Setting | Value |
|---|---|
| Takeoff position | `[-1, -1]` |
| Flight height | Adjustable (`survey_alt`, default 2.0 m) |
| Horizontal speed | 0.5 m/s |
| Yaw rate | 0.2 rad/s |
| Takeoff speed | 0.8 m/s |
| Landing speed | 0.1 m/s |
| Position tolerance | 0.1 m |
| Payload deployment height | 0.5 m above target |
| Payload hover time | 5 s |
| Landing approach | 0.5 m above marker, 5 s hover, then land |
| Target confirmation | ≥ 2 detections within 0.4 s |
| Low battery return | 20% (returns to the landing ArUco, or `[-1, -1]` if it hasn't been found) |
| YOLO model | `150 epoch Rosbag Bright 2 5 Shave` |
| Vision input | 416x416 |
| Camera FPS | 20 |
| YOLO confidence / IoU | 0.70 / 0.50 |
| Landing ArUco ID | Adjustable (`landing_aruco_id`, default 11) |

These values can be changed in:

```
src/spar/spar_node/launch/bfr2.launch
src/depthai_publisher/Models/Best_Shave/best.json
src/depthai_publisher/src/depthai_publisher/yolov5_runner_distance_est_v3.py
```

Check these settings before each assessed flight.


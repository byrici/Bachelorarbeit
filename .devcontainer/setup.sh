#!/bin/bash
set -e
set -x

echo "[1] Deleting old ROS GPG key if present"
sudo apt-key del F42ED6FBAB17C654 || true

echo "[2] Creating keyring directory"
sudo mkdir -p /usr/share/keyrings

echo "[3] Downloading and storing new ROS GPG key"
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null

echo "[4] Replacing ROS repo definition with keyring-based version"
ROS_LIST="/etc/apt/sources.list.d/ros-latest.list"
sudo bash -c "echo 'deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros/ubuntu focal main' > $ROS_LIST"

echo "[5] Updating APT"
sudo apt update

echo "[6] rosdep setup"
rosdep update
rosdep install --from-paths src --ignore-src -r -y


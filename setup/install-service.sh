#!/bin/bash
sudo cp ./robot2.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable robot2.service
sudo reboot now
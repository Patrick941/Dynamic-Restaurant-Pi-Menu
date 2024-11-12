sudo nano /etc/systemd/system/menu.service

[Unit]
Description=Menu

[Service]
ExecStart=/home/patrick/Documents/piMenu/run.sh
User=patrick
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/patrick/.Xauthority
Restart=always

[Install]
WantedBy=multi-user.target


sudo systemctl enable menu.service

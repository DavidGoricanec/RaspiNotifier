#!/bin/bash
sudo mysql -u root -p
CREATE USER $1 IDENTIFIED BY $2;
GRANT USAGE ON *.* TO $1@localhost IDENTIFIED BY $2;
GRANT ALL privileges ON `fachhochschule`.* TO  $1@localhost;
FLUSH PRIVILEGES;

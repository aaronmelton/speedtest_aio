# Speedtest All-In-One

Automatically capture your Ookla Speedtest metrics and display them in a Grafana dashboard.

![speedtest_monitor.png](speedtest_monitor.png)

## Getting Started

### About This Code
This script was written to track internet speed using Ookla's speed test.

This repository contains everything necessary to build your own Speedtest dashboard (Python script, SQLite database, Grafana dashboard).

Total application size is less than 450MB!  ~276MB for Grafana; ~153MB for Python/SQLite

Dashboard and Database data is persistent through the use of Docker Volumes.

### Prerequisites
* Docker Engine
* Docker host must be able to access Docker Hub

#### Python Libraries
* See [pyproject.toml](pyproject.toml)

### Instructions For Use

* Clone this repository.
* Modify the `speedtest_aio-cron` file to adjust your test interval.  The default is 15 minutes.  Visit [crontab.guru](https://crontab.guru) for an example on cron scheduling syntax.
* Modify the Test Results panel in Grafana to match the values for your Internet connection.  The default is set to 75Mb/s down and 25Mb/s up (which happen to be my Internet speed).
  Edit the Test Results panel, goto the Overrides and change the Max values for all Overrides to fit your situation.  (This will change the gradient levels for download_throughput, upload_throughput and ping_latency.)

#### Docker Commands

* To pull/build the necessary Docker images:
`docker-compose build`

* To run the application:
`docker-compose up -d`

* To stop the application:
`docker-compose down`

#### Grafana

* Default username/password is admin/admin.
* You will be prompted to change your password upon first login.
* Access your Grafana dashboard via [http://localhost:3000](http://localhost:3000) OR replace localhost with the IP Address of the host.
* **WARNING** This dashboard will be accessible to all hosts in the same subnet!

## Acknowledgements
* Grafana dashboard layout borrowed from [speedtest_exporter](https://github.com/danopstech/speedtest_exporter).

## Authors
* **Aaron Melton** - *Author* - Aaron Melton <aaron@aaronmelton.com>

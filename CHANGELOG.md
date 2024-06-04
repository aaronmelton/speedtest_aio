# CHANGELOG

## [0.6.2] - 2024-06-04
### Fixed
- Dockerfile-speedtest-RPi: Incorrect path specified for poetry install in test image.


## [0.6.1] - 2024-05-17
### Fixed
- Added secure option to the speedtest command.  (This is why we can't have
  nice things.)


## [0.6.0] - 2024-05-17
### Added
- docker-compose-RPi.yml: Adding file specifically for use with Raspberry Pis.
### Changed
- Bumping Python to 3.12 and updating all library versions.
- Dockerfile-grafana: Updating grafana 10.2.2 -> 10.2.7
- Dockerfile-speedtest: Updating supercronic 0.2.27 -> 0.2.29
- Dockerfile-speedtest-RPi: Updating Debian buster -> bookworm;
  supercronic 0.2.27 -> 0.2.29; Bringing this file more in line with
  Dockerfile-speedtest.
- README.md: Updating instructions for using Raspberry Pi Dockerfile.
- docker-compose.yml: Removed deprecated version statement.


## [0.5.1] - 2023-11-26
### Changed
- pyproject.toml: Rolling back Python version to 3.11.  v3.12 not in widespread
  use yet...


## [0.5.0] - 2023-11-24
### Fixed
- grafana/grafana_dashboard.json: Updated dashboard JSON which should fix
  Issues #2 and #4.
### Added
- .dockerignore: If we're building Docker Images, we should probably have
  one of these...
- tests/test_class_Config.py: Poor excuse for a unit test file.
### Changed
- .gitignore: Updating project-specific files.
- docker-compose.yml: Switching default speedtest_aio Docker file from
  Dockerfile-speedtest-RPi to Dockerfile-speedtest. 
- Dockerfile-grafana: Pinning to version 10.2.2.
- Dockerfile-speedtest: Switching Docker image from Alpine to Python because
  it's easier to work with.
- entrypoint.sh: Correcting path for Supercronic bin.
- README.md: Minor clarification to the instructions.
- pyproject.toml: Bumped Python to v3.12; Python functions consolidated into
  a new code repository, aaron-common-libs, which is now imported into this
  script; speedtest-cli is now installed via Poetry; Bumped all development
  test packages to latest versions.
- speedtest_aio/config.py, speedtest_aio/speedtest_aio.py: Refactored most
  functions: Config, logging setup, SQL calls.


## [0.4.4] - 2022-02-23
### Changed
- Improving functionality that times app from using time.time() to 
  time.perf_counter().
- Dockerfile-speedtest-RPi: Modified based on user feedback.
- Updating Python libraries.


## [0.4.3] - 2022-02-23
### Changed
- Dockerfile-speedtest: Put prune label in the wrong place.


## [0.4.2] - 2022-02-22
### Changed
- README.md: Improved spacing for Docker commands.
- Updating click (8.0.3 -> 8.0.4)
- Updating gitpython (3.1.26 -> 3.1.27)
- Updating platformdirs (2.4.1 -> 2.5.1)
- Updating typing-extensions (4.0.1 -> 4.1.1)


## [0.4.1] - 2022-02-22
### Changed
- Dockerfile-speedtest: Added prune label to the base image build.
- grafana/grafana_dashboard.json: Sorting test list by descending time.
- README.md: Improved instructions for Docker operation.
- speedtest_monitor.png: New screenshot to reflect new layout.


## [0.4.0] - 2022-02-21
### Changed
- docker-compose.yml: Updating paths to match changes in application.
- Dockerfile-grafana: Added ownership flags to COPY command.
- Dockerfile-speedtest-RPi: Replacing speedtest_aio-cron with crontab.
- Dockerfile-speedtest: Updated for use in Alpine Linux.
- grafana/datasource.yml: Updating paths to match changes in application.
- grafana/grafana_dashboard.json: Updating to match changes to code.
- README.md: Improved instructions for Docker operation.
- speedtest_aio-cron: Updated for use in Alpine Linux.
- speedtest_aio.py: create_database(): Removed fields that are no longer being tracked.


## [0.3.1] - 2022-02-07
### Changed
- pyproject.toml: Updating pbr (5.8.0 -> 5.8.1)
- pyproject.toml: Moved development-only packages into [tool.poetry.dev-dependencies]


## [0.3.0] - 2022-02-03
### Added
- docker-compose.yml
- Dockerfile-grafana
- Dockerfile-speedtest
### Changed
- Forked speedtest_monitor v0.2.0 to change database type from MySQL to SQLite
  and create a single-image Docker Container.
- Renamed project: speedtest_monitor -> speedtest_aio
- create_database(): Added to check for existence of database/table.
- db_query(): Altered to support SQLite syntax.
### Removed
- config.py: Removed environment variables.  What were variables are now
  statically defined so Docker and Grafana provisioning know where to find them.


## [0.2.0] - 2022-01-24
### Added
- Added schema structure to the project.
- Added Grafana dashboard export to the project.
- pyproject.toml[bandit]: Ignoring info-warnings about subprocess.
### Changed
- Switched from using Silva's speedtest-cli to Ookla's speedtest CLI binary.
  Both produce JSON format output that can be collected.  Decided to switch to
  Ookla's binary since the vendor provides JSON output too.
- README.md: Updated to reflect changes in the project; Included screenshot of
  dashboard.
- speedtest_list{} and SQL table also had to change to capture additional
  information Ookla's JSON output provided that I wanted to capture.


## [0.1.0] - 2022-01-16
### Added
- Creating a new project to collect speedtest.net results and store them in a
  database.

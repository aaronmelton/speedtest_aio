# CHANGELOG

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

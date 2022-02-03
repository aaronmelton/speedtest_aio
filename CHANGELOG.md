# CHANGELOG

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

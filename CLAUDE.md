# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project that uses the Navitime Reachable API to find stations and bus stops within a specified travel time from a given location. The application:
- Finds stations/bus stops reachable within 30 minutes (configurable) from Kayabacho station
- Filters by number of transfers (e.g., max 1 transfer)
- Exports results to CSV files
- Visualizes the reachable area on an interactive map

## Development Setup

This project uses mise for Python environment management and Poetry for dependency management.

### Prerequisites
```bash
# Install mise (if not already installed)
# See: https://mise.jdx.dev/

# Activate mise environment
mise install

# Install dependencies
poetry install
```

## Common Commands

### Dependency Management
```bash
# Install all dependencies
poetry install

# Add a new dependency
poetry add <package>

# Add a development dependency
poetry add --group dev <package>

# Update dependencies
poetry update
```

### Running the Application
```bash
# Activate the virtual environment
poetry shell

# Run Python scripts
python src/main.py  # (when main.py is created)
```

### Environment Variables
The project uses the Navitime Reachable API which requires an API key. Set the following environment variable:
```bash
export RAPIDAPI_KEY="your_api_key_here"
```

## Project Structure

- `src/` - Main source code directory (currently empty, to be populated)
- `csv/` - Output directory for CSV files
- `pyproject.toml` - Poetry configuration and dependencies
- `mise.toml` - Python version management (Python 3.13.3)

## Key Dependencies

- **requests**: HTTP client for API calls
- **pandas**: Data manipulation and CSV handling
- **geopandas**: Geospatial data processing
- **shapely**: Geometric operations
- **folium**: Interactive map visualization

## API Integration

The project uses the Navitime Reachable API via RapidAPI:
- Endpoint: `https://navitime-reachable.p.rapidapi.com/reachable_motorcycle`
- Required headers: `x-rapidapi-host` and `x-rapidapi-key`
- Key parameters: start coordinates, travel time limit, partition count
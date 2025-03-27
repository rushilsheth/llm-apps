# toy_apps Module

The `toy_apps` module contains demonstration applications showcasing various AI capabilities. Currently, the repository includes two main applications:

## Structure
```
toy_apps/
├── __init__.py
├── ai_DA/
│   ├── main.ipynb
│   └── soci_econ_country_profiles.csv
└── turboseek/
    ├── __init__.py
    ├── brave_search.py
    ├── search_app.py
    └── together_client.py
```

## Applications

### AI Data Analysis (ai_DA)
A Jupyter notebook-based application for analyzing socioeconomic country profiles data. The application demonstrates how to use AI to gain insights from structured data.

**Files:**
- [`main.ipynb`](ai_DA/main.ipynb): Interactive notebook with data analysis workflows
- [`soci_econ_country_profiles.csv`](ai_DA/soci_econ_country_profiles.csv): Dataset containing socioeconomic indicators for different countries

### TurboSeek
A search application that combines the Brave Search API with Together AI's language models to provide enhanced search capabilities.

**Files:**
- [`__init__.py`](turboseek/__init__.py): Package initialization file
- [`brave_search.py`](turboseek/brave_search.py): Integration with Brave Search API
- [`search_app.py`](turboseek/search_app.py): Main application logic
- [`together_client.py`](turboseek/together_client.py): Client for interacting with Together AI's language models

### Environment Variables
Some applications may require API keys:
- `TOGETHER_API_KEY` for Together AI integration
- `BRAVE_API_KEY` for Brave Search integration

## Usage
Refer to individual application directories for specific usage instructions.

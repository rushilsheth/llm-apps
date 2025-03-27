# TurboSeek Module

The `turboseek` module is a search application that combines the Brave Search API with Together AI's language models to provide enhanced search capabilities.

## Structure
```
turboseek/
├── __init__.py
├── brave_search.py
├── search_app.py
└── together_client.py
```

## Components

### Brave Search Integration (`brave_search.py`)
Handles interaction with the Brave Search API to retrieve search results based on user queries.

### Together AI Integration (`together_client.py`)
Uses Together AI's language models to generate comprehensive responses based on search results.

### Main Application (`search_app.py`)
The Gradio-based application that ties together the Brave Search and Together AI integrations to provide a user-friendly interface for performing searches and viewing results.

## Environment Variables
The following environment variables are required for the application to function:
- `BRAVE_API_KEY`: API key for Brave Search integration.
- `TOGETHER_API_KEY`: API key for Together AI integration.

## Usage
Run the Gradio application:

```bash
python search_app.py
```

## Features
- **Search Results**: Retrieves search results from Brave Search.
- **AI-Powered Responses**: Generates detailed responses using Together AI's language models.
- **Interactive Interface**: User-friendly Gradio interface for seamless interaction.

## Notes
Ensure that the required API keys are set in your environment before running the application.

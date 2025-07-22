# FlixSearch - Movie & TV Discovery App

## Overview

FlixSearch is a desktop application built with Flet that allows users to search for movies and TV shows using the TMDB (The Movie Database) API. The app features a Netflix-inspired UI with dark theme, responsive design, and detailed information display.

![Screenshot 1](https://lakiup.com/wp-content/uploads/2025/07/4.png)
*Main search interface*

![Screenshot 2](https://lakiup.com/wp-content/uploads/2025/07/5.png)
*Search results display*

![Screenshot 3](https://lakiup.com/wp-content/uploads/2025/07/6.png)
*Detailed view modal*

## Features

- Search for movies and TV shows
- Toggle between movie and TV show content types
- View detailed information about each title
- See ratings and overviews
- Open TMDB page for more information
- Responsive design that works on different screen sizes
- Netflix-inspired UI with dark theme

## Prerequisites

- Python 3.7+
- Flet library
- TMDB API key

## Installation

1. First, install the required dependencies:

```bash
pip install flet requests
```

2. You'll need to get an API key from TMDB:
   - Go to [The Movie Database website](https://www.themoviedb.org/)
   - Create an account if you don't have one
   - Request an API key from your account settings

## Configuration

Replace the placeholder API keys in the code with your actual TMDB API credentials:

```python
# API Configuration
API_KEY = "your_api_key_here"  # Replace with your actual API key
API_READ_ACCESS_TOKEN = "your_read_access_token_here"  # Replace with your actual read access token
```

## Running the Application

To run the application, simply execute the Python script:

```bash
python flixsearch.py
```

## Usage

1. **Searching for Content**:
   - Select either "Movies" or "TV Shows" using the toggle buttons
   - Enter your search query in the search field
   - Press Enter or click the "Search" button

2. **Viewing Details**:
   - Click on any result card to view detailed information
   - The modal will show the backdrop image, title, rating, and overview
   - Click "View on TMDB" to open the item's page on The Movie Database website
   - Click the close button or the overlay to close the modal

3. **Switching Content Types**:
   - Use the "Movies" and "TV Shows" buttons to switch between content types
   - The search will automatically update to show the selected content type

## Code Structure

The application is structured as a single class `TMDBApp` with the following main components:

1. **UI Setup**:
   - `setup_ui()` - Creates the main application interface
   - `create_details_modal()` - Creates the modal for detailed information

2. **Functionality**:
   - `change_content_type()` - Handles switching between movies and TV shows
   - `search_content()` - Performs the API search
   - `create_result_card()` - Creates individual result cards
   - `show_details()` - Shows detailed information in the modal
   - `close_modal()` - Hides the details modal
   - `open_tmdb_page()` - Opens the TMDB website for the selected item

3. **Helper Methods**:
   - `card_hover_effect()` - Adds hover animations to result cards

## Customization

You can customize the app by modifying the following:

1. **Colors**:
   - The color scheme is defined in the `colors` dictionary in the `__init__` method

2. **Layout**:
   - Adjust the window dimensions in the page configuration
   - Modify the grid view parameters for different result layouts

3. **API Parameters**:
   - Change the language or other API parameters in the search request

## Troubleshooting

1. **No Results Appearing**:
   - Check your internet connection
   - Verify your API keys are correct
   - Ensure you have the latest version of the requests library

2. **Images Not Loading**:
   - Some items might not have poster images - these will show a placeholder icon
   - Check if the TMDB image URLs are accessible

3. **Application Not Starting**:
   - Make sure all dependencies are installed
   - Check for Python version compatibility

## License

This project is open-source and available for personal use. For commercial use, please check TMDB's API terms of service.

## Acknowledgments

- The Movie Database (TMDB) for their excellent API
- Flet team for the Python UI framework

---

For any issues or feature requests, please open an issue on GitHub. Contributions are welcome!

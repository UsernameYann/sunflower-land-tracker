# Sunflower Land Data Tracker

A graphical application for tracking and visualizing resources in Sunflower Land.

## Dependencies

This application uses the following libraries:

- tkinter (included with standard Python)
- matplotlib (BSD license)
- numpy (BSD license)
- requests (Apache 2.0 license)
- schedule (MIT license)
- mplcursors (MIT license)

## API Usage Notice

This application interacts with the Sunflower Land public API. Please respect rate limits and API usage policies.

This is an unofficial tool that is not affiliated with, endorsed by, or related to Sunflower Land or its creators.

## Installation

1. Make sure you have Python installed (version 3.6 or higher)
2. Install the required dependencies:
```
pip install matplotlib numpy requests schedule mplcursors
```
3. Clone or download this repository
4. Run the application:
```
python3 gui.py
```

## How to Use

### Getting Started
1. Enter your Farm ID in the input field
2. Click "Validate" to load your farm data
3. If this is your first time, you'll be prompted to perform an initial data save
4. Choose whether you want automatic daily updates

### Main Functions

#### Graph Tab
- View graphical representations of your farm resources
- Filter data by various categories (Balance, Vegetables, Fruits, etc.)
- Select specific items to display within categories
- Filter by time period: all history, last 7 days, last 30 days or custom period
- Hover over data points to see detailed information and value changes

#### Farm Management Tab
- View and manage your saved farms
- Switch between different farms by double-clicking on farm IDs
- Toggle automatic updates for any farm
- Remove farms from auto-update or manual lists
- Perform manual updates when needed

### Automatic Updates
- Farms can be set for automatic daily updates at midnight
- The app indicates when the next automatic update is scheduled
- Status indicators show whether auto-update is enabled or disabled

### Manual Updates
- Click "Manual Update" to update data on demand
- You can update once per day (overwriting is possible with confirmation)

## File Structure
- The data is saved in JSON format in the "data" directory
- Each farm has its own folder named after its Farm ID
- Daily updates are saved as YYYY-MM-DD.json files

## Troubleshooting
- If the app shows "API Connection: Error", check your internet connection
- Make sure the Farm ID is entered correctly
- For any errors during updates, check the console output for details

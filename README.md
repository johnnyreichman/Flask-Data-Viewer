# Flask-Data-Viewer
Basic flask app to view some data.
This web application is separated into two views:

The first view displays a line graph with any state's senate, house, or presidential election results over time. Users select the state and race via a dropdown and the graph updates to reflect the selection.
![alt text](https://github.com/johnnyreichman/Flask-Data-Viewer/blob/main/screenshots/example_illinois_historical.png?raw=true)

The second view is a basic dashboard with two interesting insights--a pie chart showing the distribution of Congressional term lengths and a bar graph comparing Illinois voter turnout over time and between races.
![alt text](https://github.com/johnnyreichman/Flask-Data-Viewer/blob/main/screenshots/example_dashboard.png?raw=true)


Data comes from https://electionlab.mit.edu/data.

To access the application:
1. Run the server by navigating to the directory and running:
"python3 main.py" (or whatever version of python you have)
2. Navigate to the localhost URL Flask is configured to show

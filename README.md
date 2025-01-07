# Rock Radar

# Tech Stack
- **Language:** Python 3.11
- **Libraries & Frameworks**:
    - PyQt5: For building the GUI
    - Requests: For making HTTP requests to fetch online data
    - BeautifulSoup: For parsing and extracting data from HTML

# Key Features

## Sorting
<img src='./pictures/filtered-areas-sorted.png'>

# Installation
## Cloning
```bash
git clone https://github.com/rmejia4209/Rock-Radar.git
```
## Installing Dependencies
```bash
cd Rock-Radar
pipenv install
```
## Setting Up `scraper.py`
The scraper.py script is designed to obscure the data source by dynamically
loading parsing tags from a .env file, reducing the visibility of the target
structure within the codebase. For the project to be fully functional, either
the parsing tags in the .env file must match the structure of the source
website, or data conforming to the format defined in custom_data.py should be
provided.Please note that I do not condone unethical web scraping. Always
review and adhere to a website’s terms of service and respect the ethical
guidelines of data usage.


# Future Improvements
- **Speed Optimizations**
    - The current implementation uses Python 3.11, which does not support true parallelization due to the Global Interpreter Lock (GIL). Upgrading to
    Python 3.12 (when versions with better concurrency are available) could
    potentially allow for true parallelization, improving performance.
    - In preliminary tests with 260,000 routes, the load time was around 5
    seconds. Interestingly, Python 3.11's threaded execution reduced the load
    time by 16% with 25,000 routes, likely due to the overhead of setting up parallelization and accessing the GIL.
    - The data tree is currently calculated and sorted in the main thread, and
    it could be a candidate for parallelization to further reduce processing
    time and improve efficiency.
- **Persistence of Settings**
    - Implementing a way to persist user settings, such as preferences or
    configurations, would enhance user experience by maintaining their choices
    across sessions.
- **UI Tweaks**
    - While the current UI works, it could benefit from visual improvements.
    UI design is not my strongest point, and I prioritized finalizing the app's functionality before focusing on the user interface. Future work will
    involve refining the layout, design, and overall user experience.
- **Add a dedicated Database**
    - Currently, data is stored in a combination of .csv and .json files.
    Introducing a database would improve data management and scalability. A
    lightweight, embedded solution like SQLite would be an appropriate choice
    for this project, offering simplicity and minimal overhead without the need
    for additional server setup
- **Standardize Documentation**
    - Many functions lack docstrings or use inconsistent formats. Adopting a
    uniform style, such as PEP 257, would improve clarity and maintainability.

# Credits
## Icons
- [Back icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/back)
- [Gear/Setup icons created by Saepul Nahwan - Flaticon](https://www.flaticon.com/free-icons/setup)
- [Home button icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/home-button)
- [Warning icons created by Good Ware - Flaticon](https://www.flaticon.com/free-icons/warning)
- [Success icons created by Arkinasi - Flaticon](https://www.flaticon.com/free-icons/success)

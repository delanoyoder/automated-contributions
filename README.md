# GitHub Contribution Graph Automator

## Description

Welcome to the GitHub Contribution Graph Automator repository! This project automates contributions by executing a daily cron job that pushes commits to a dummy repository. This way, your GitHub contribution graph can visually spell out a message, pattern, or design of your choosing on days deemed fit. Perfect for having fun with your contribution graph while also learning and experimenting with cron jobs and Git automation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Features

- Automated daily commits to a dummy GitHub repository.
- Customizable patterns for contribution graph.
- Easily enable or disable the cron job.

## Installation

To clone and run this repository, you'll need [Git](https://git-scm.com) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/delanoyoder/automated-contributions

# Go into the repository
$ cd automated-contributions

# Install dependencies (only supported for Unix systems)
$ ./setup.sh
```

## Configuration

1. **Set Up Dummy Repository:**
   - Create a dummy repository on your GitHub account. (can be private)
   - Link the dummy repository in the configuration file of this project.

2. **Design Your Graph:**
   - Plan and design your desired pattern or message for the contribution graph.
   - Configure the dates in the configuration file to match your design.

3. **Configure Cron Job:**
   - Set up the cron job on your machine to run the script daily.
   - Additional instructions are provided in the repository documentation.

## Usage

After completing the configuration, the cron job will automatically run daily and push commits to the dummy repository on the dates specified in your design. Monitor your contribution graph on your GitHub profile to view the evolving design.

```bash
# Create a your custom contribution graph and cron job
$ python scheduler.py

# Check what your contribution graph looks like (optional)
$ python display.py --config configs/<name_of_your_config_file.json>
```

## Contribute

We welcome contributions to improve the functionality and features of this project:

- Fork the repository
- Create a feature branch (`git checkout -b feature_branch`)
- Commit your changes (`git commit -am 'Add some feature'`)
- Push to the branch (`git push origin feature_branch`)
- Submit a Pull Request

## License

This project is open-source and available under the MIT License. See the [LICENSE.md](LICENSE.md) file for more details.

## Contact

If you have questions or concerns, please open an issue or contact the maintainers at dayoder4@gmail.com. Enjoy automating your GitHub contribution graph with ease and style!

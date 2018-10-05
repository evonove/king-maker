King Maker
==========

Kickstarter's comments scraper.

### Requirements

* Python 3.6
* pipenv 2018.7.1
* geckodriver v0.23.0

`pipenv install` to install dependencies, you also need [geckodriver](https://github.com/mozilla/geckodriver/releases) otherwise browser would not load.

### Usage

To run the script:

    pipenv shell
    python kingmaker.py https://www.kickstarter.com/projects/tabulagames/mysthea/comments output.txt

It takes its time in case there are loads of comments, be patient.

### Code style

`black` is used for code formatting using arguments `--line-length 100 --py36`.

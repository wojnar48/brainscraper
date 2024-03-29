## Running container

```
# Build docker image
docker build -t fantasy-scraper:latest .

# Run container
docker run -v "$PWD":/usr/src/app -it fantasy-scraper:latest

# Inside container, activate scraper-env python venv
source scraper-env/bin/activate
```

## Running scraper
The scraper takes a start date and number of days for which to scraper data

>**Note:** To see list of available flags and arguments run: `rotoscraper --help`

>**Note:** If `rotoscraper` command is not available see [Installation instructions](#installation-instructions)

```
# Example: To scrape 1 day of data on 2019-06-04 run:
rotoscraper --numdays 1 2019-06-04 
```

## Installation instructions
To install `rotoscraper` run:

>**Note:** Make sure the `scraper-env` is activated

```
pip install --editable .
```
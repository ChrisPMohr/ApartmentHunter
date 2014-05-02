# ApartmentHunter

## Overview

ApartmentHunter is a Python 3 application that loads recent apartment listings from craigslist.org, extracts features from them, and stores them in a MongoDB database.


## Features

Data extracted from each listing includes:
* Price
* Address
* Available date
* Phone number
* Number of bedrooms


## Installation

```
pip install -r requirements.txt
```


## Usage

```
python ./listing_finder.py --name [NAME] --url [URL] -n [N]
```
will search the apartment listings at the craigslist page at URL for N new listings and save them to the MongoDB collection NAME.

#### Example

```
python ./listing_finder.py --name Pittsburgh --url http://pittsburgh.craigslist.org/apa/ -n 20
```

ApartmentHunter requires MongoDB running on the default port on the local machine.

## Tests

ApartmentHunter has a suite of unit tests that can be ran from the top level directory with

```
python -m tests.listing_tests
```

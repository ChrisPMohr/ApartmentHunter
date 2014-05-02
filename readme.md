# ApartmentHunter

## Overview

ApartmentHunter is a Python 3 application that loads recent apartment listings from craigslist.org, extracts features from them, and stores them in a MongoDB database.

## Usage

python ./listing_finder.py --name [NAME] --url [URL] -n [N]

will search the apartment listings at the craigslist page at URL for N new listings and save them to the MongoDB collection NAME.

This requires MongoDB running on the default port on the local machine.

## Installation

pip install -r requirements.txt

## Features

Data extracted from each listing includes:
* Price
* Address
* Available date
* Phone number

Future features to be extracted include:
* Number of bedrooms
* Email address
* Presence of pictures
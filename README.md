# dsa-data

This repository includes data related to the Democratic Socialists of America (DSA), specifically regarding the constitutional boundaries of different chapters.

# Manifest

- **scraper:** this folder contains a python script to scrape the DSA website for every ZIP code and save the results to a .csv. **It is intentionally incomplete, and I advise against using it unless this repo is extremely out-of-date.**
- **shapefiles:** this folder contains shapefiles for DSA chapters based on ZIP codes scraped from the DSA website in a .csv also within this repo. They can be loaded in QGIS, ARCGIS, and other GIS tools. I recommend using a map sublayer like OSM standard given they do not cover the entire country. The only attribute for them presently is the chapter name (as listed in DSA's internal system, eg. Rhode Island DSA is still Providence DSA) but more such as chapter size, population, website, etc will be added soon.
- **chapter_zips.csv:** this is the current chapter ZIP .csv as scraped in June 2023. It may or may not be accurate to the present, and may or may not include instances of human error. A more updated one will be scraped by mid-September.
- **dsa-chapters.png:** a super high-res image of the DSA chapter map for those unable or unwilling to use GIS. This is a very large image, and may take some time to load.
- **first-preference-by-chapter.png:** an example use case for this data, a map created by me showing each chapter's first preference pick for DSA NPC at the 2023 convention. Once again this is a very large image, and may take some time to load.
- **LICENSE-CC-BY:** Creative Commons Attribution 4.0 International License. See below.

# License
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
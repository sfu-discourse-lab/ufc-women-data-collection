# Women in UFC

This project aims to analyze the differences between the way women and men fighters are talked about in news articles published on the UFC website.
This specific repository focuses on data collection and cleaning.

The process is split up into separate Jupyter notebook files to run in sequence. Python 3.12 is recommended.

## Setting up your environment

### Installing packages

There is a notebook called 00_install_dependencies.ipynb which you can run to install all the dependencies you need for this project.

## Running the pipeline

There does not seem to be a UFC API to easily get articles from their website, so we have to use web crawling and scraping to get the data.

If you are using `venv`, make sure that you select the correct kernel called `venv (Python 3.12.10)` (or whatever version of Python you have installed) when you run the following Jupyter notebooks.

### 1. Downloading article links

As of September 2025, the [UFC news website](https://www.ufc.com/trending/all) is organized in a 3 by 5 grid (roughly) of articles, sorted by newest article first. You can access more articles by either clicking the "Load More" button at the bottom, or manually navigating to a specific page by typing the URL `https://www.ufc.com/trending/all?page=<page number>`. First and foremost, the scraper goes to a large number of pages, where it downloads some basic data from the grid of articles (more below).

Open the file `01_download_article_links.ipynb` in a Jupyter notebook.
Find the variable called `num_pages_to_get` and set it to the number of pages you want to it to scrape. Each page has about 15 article links, so keep this in mind. When I ran the scraper on 16 Sept. 2025 with `num_pages_to_get = 200`, the oldest article I got was from 12 Jan. 2025, so adjust accordingly to your desired date range.

This scraper gets basic information about the articles like the link, headline, article type, and how long ago it was posted (as shown by the text on the page, e.g. "2 months ago").

When you finish running this notebook, this data will be saved to a file called `article_links_<date and time>.csv`. You can view this file in Excel, and it will also be used in the following steps to scrape the article contents themselves.

### 2. Downloading article contents

Open the file `02_download_article_contents.ipynb` in a Jupyter notebook.
Find the variable `filename` and change it to the name of the file you just downloaded from the previous step.

This scraper runs for articles of type "Results", "Athletes", "Fight Coverage", and "Fight Preview", and excludes any video or gallery pages.

This step is pretty simple because it doesn't yet extract data from the articles into a useful format, but rather simply downloads the contents of the articles to be stored on your computer.

When you finish running this notebook, it will create a new file called `article_links_<date and time>_with_contents.csv`, which will be used in the following steps.

### 3. Extracting data

Open the file `03_extract_article_data.ipynb` in a Jupyter notebook. Find the variable `filename` and change it to the name of the file you just downloaded from the previous step.

This notebook extracts metadata and text from the articles previously downloaded. The data it extracts includes:

- Title (usually the same as the headline)
- Description
- Published time
- Last modified time
- Author
- Author's social media handle (usually their X/Twitter profile)
- Article text and image captions (the images themselves can be downloaded in the next steps)

There are two main files saved in this step: `article_links_<date and time>_with_contents_with_data.csv`, which includes all of the data extracted from this step, and `article_links_<date and time>_with_only_metadata.csv` which only has the metadata so that it's easier to look through.

Additionally, the text of each article is stored into its own txt file in the `./articles` directory, with the name of the file corresponding to the article link; for example, the text for [https://www.ufc.com/news/live-results-official-scorecards-match-recaps-interviews-canelo-vs-crawford-las-vegas](https://www.ufc.com/news/live-results-official-scorecards-match-recaps-interviews-canelo-vs-crawford-las-vegas) will be stored in `./articles/news_live-results-official-scorecards-match-recaps-interviews-canelo-vs-crawford-las-vegas.txt`.

### 4. Downloading images from articles

If you want to also download images from the previous articles, this step does it.

Open the file `04_download_images_from_articles.ipynb` in a Jupyter notebook. Find the variable `filename` and change it to the name of the `article_links_<date and time>_with_contents_with_data.csv` file you just downloaded from the previous step.

This step finds all the images on each page and downloads them. As you can imagine, it takes quite a long time to run this on a large number of articles, so be patient. Thankfully, this notebook is quite simple.

When you finish running this notebook, all the images will be downloaded to the `./images` directory, with further subdirectories created for each article.

### 5. Downloading images from galleries

If you also want to download the images from the special photo gallery pages, this step does it. It is very similar to the previous step.

Open the file `05_download_images_from_galleries.ipynb` in a Jupyter notebook. Find the variable `filename` and change it to the name of the `article_links_<date and time>.csv` file from step 1.

When you finish running this notebook, it will also download images to subdirectories within the `./images` directory.

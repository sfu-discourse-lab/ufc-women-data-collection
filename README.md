# Women in UFC

This project aims to analyze the differences between the way women and men fighters are talked about in news articles published on the [UFC website](https://www.ufc.com).
This specific repository focuses on data collection and cleaning.

The process is split up into separate Jupyter notebook files to run in sequence. Python 3.11 is recommended.

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

### 6. Separating gendered paragraphs

To split up articles into paragraphs that talk about people of different genders, use the notebook `06_separate_gendered_paragraphs.ipynb`.

This will get all of the article content files and split up their paragraphs into 4 different types:

- Men: paragraphs that are primarily about men
- Women: paragraphs that are primarily about women
- Equal: paragraphs that have equal mentions of men and women
- Genderless: paragraphs that have no mentions of men or women

These separated paragraphs are saved into subfolders within the `./articles` folder, with the folder name being the name of the original text file.

It does this by finding all the names in each article, scraping their UFC fighter profile, and getting from the profile whether they're a male or female fighter.

Then it counts the number of mentions of men and women names, pronouns, and other coreferences using the `coreferee` library.

If there are more women than men mentioned, it is a woman paragraph, and vice versa.

### 7. Organizing the corpus

The previous step creates a subfolder for each article, and creates `equal.txt`, `genderless.txt`, `man.txt`, and `woman.txt` for each article.

This step can sort of reverse the hierarchy where there are just 4 folders within a `corpus` folder representing each separation,
and separate txt files within the folders for each article.

### 8. Creating a sample annotation corpus

This step creates a sample corpus for testing annotation, containing 5% of the total corpus articles. Choosing which articles go into the sample corpus is not done by random, but it follows specific criteria.

First we take articles that are within one standard deviation of the average (median) number of tokens. This makes sure that the articles in the sample corpus are not too long or too short, and represent the "average" article one may encounter in the overall corpus, as this is meant to be a representative sample.

Then for the man- and woman-focused sample articles, the ones with the highest proportion of man- and woman-focused paragraphs (respectively) to total number of paragraphs are the ones that get chosen for the sample corpus. This is also the case with the genderless articles.

For articles whose paragraphs are equally man- and woman-focused, the process is exactly the same. However, note that most of the paragraphs in most of the articles focus on one person (usually a man), so there are few instances of truly equal paragraphs. Therefore, even the most "equal" articles have a moderate gender preference, so they are not truly "equal".

Finally, we look for the most "balanced" articles. _Balanced_ here means that there is an equal (or as close to as possible) number of man-focused, woman-focused, equal, and genderless paragraphs. To try to achieve this balance, we first take out any "Athlete" type articles, which are articles that highlight one particular fighter, and are therefore extremely focused on one gender. Then, we calculate three measures that indicate balance in our definition, applied to the proportion of man paragraphs, proportion of woman paragraphs, proportion of equal paragraphs, and proportion of genderless paragraphs per article:

1. **Entropy**: this measures uncertainty in a probability distribution, or in our case, balance between input values. Higher entropy means more balanced and lower entropy means less balanced. So we try to find articles with the highest entropy.
2. **Variance**: this is another probability-related term that measures a variable's "distance" from some target value. In our case, we measure variance from the target value of 0.25, which would mean perfectly balanced between four variables. Lower variance means more balanced and higher variance means less balanced. So we try to find articles with the lowest variance.
3. **Absolute difference from mean number of tokens**: this one is simple, just calculating the absolute value of the difference of each article's number of tokens from the mean number of tokens. Higher token difference is further from the mean and lower token difference is closer to the mean. Here, we actually try to achieve higher token difference because this would allow for more varied sample articles with different lengths and potentially different styles due to this variance. However, this is still fine because, as mentioned previously, we only consider articles that are within one standard deviation of the overall corpus article length. So this will not yield any insane differences in article lengths, but some slight variation to get a more diverse sample distribution. Since we don't care about this measure as much as the previous two, we multiply it by a factor that reduces its imapct in the balance score calculation.

We take the top articles from each of these 5 categories (man, woman, equal, genderless, balanced) and put them in their respective folders (`sample_corpus/mostly_man`, `sample_corpus/mostly_woman`, `sample_corpus/mostly_equal`, `sample_corpus/mostly_genderless`, `sample_corpus/balanced`).

Then, we create a backup sample corpus with the same structure and criteria, stored in the folder `sample_corpus_backup`. Note that the articles in here will be less gendered or less balanced because they are basically the "leftovers" from the original sample corpus. This one is also 5% of the full corpus.

### 9. Calculating and visualizing sentiment

This step calculates polarity and subjectivity for the different subcorpora (man, female, equal, genderless, and OVERALL) using spaCy.
Polarity is also separated into only positive examples and only negative examples to see how extreme each subcorpus gets. It outputs the figures for these calculations to the `figures/` folder.

### 10. Calculating paragraph vocabulary counts

This step counts the number of times certain nouns and adjectives appear in each paragraph, split by subcorpus (man, woman, equal, genderless). Furthermore, it counts the paragraph lengths (number of tokens) and calculates polarity using spaCy. It outputs these stats to `./paragraph_stats.csv`.

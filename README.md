# Book Price Scraper

A small Python project that collects book data from [Books to Scrape](https://books.toscrape.com), a website made for practicing web scraping.

## What it does

- Visits the first 3 catalogue pages (60 books)
- Collects the title, price, star rating, stock status, and link of each book
- Saves everything to `books.csv`
- Prints the cheapest book and the average price

## Tools

- Python 3
- [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) to read the HTML
- [Requests](https://requests.readthedocs.io/) to download the pages

## How to run

```bash
git clone https://github.com/ciputrii21/book-price-scraper.git
cd book-price-scraper
pip install -r requirements.txt
python3 scraper.py
```

## Output

The script creates `books.csv` with these columns:

| Column | Meaning |
|---|---|
| title | Book title |
| price_gbp | Price in British pounds |
| rating | Star rating, from 1 to 5 |
| stock | Stock status |
| url | Link to the book page |

## What I learned

- How to find data in HTML with `select()` and `find_all()`
- How to read multi-valued attributes such as `class`
- How to loop through several pages politely, with a short delay
- How to save scraped data to a CSV file

## Notes

Books to Scrape is a sandbox site built for scraping practice. Always check the rules (Terms of Service and `robots.txt`) before scraping a real website.

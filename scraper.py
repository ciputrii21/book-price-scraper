"""Book Price Scraper: collect book data from books.toscrape.com and save it to CSV."""

import csv
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
PAGES = 3            # 3 halaman x 20 buku = 60 buku
DELAY_SECONDS = 1    # jeda antar permintaan supaya sopan ke server
HEADERS = {"User-Agent": "belajar-bs4/1.0 (learning project)"}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
FIELDS = ["title", "price_gbp", "rating", "stock", "url"]


def fetch_page(url):
    """Unduh satu halaman lalu ubah jadi objek soup."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def parse_book(card, page_url):
    """Ambil data dari satu kartu buku (<article class="product_pod">)."""
    title = card.h3.a["title"]

    price_text = card.select_one("p.price_color").get_text(strip=True)
    price = float(re.sub(r"[^0-9.]", "", price_text))  # sisakan angka dan titik saja

    rating_classes = card.select_one("p.star-rating")["class"]  # ['star-rating', 'Three']
    rating = RATING_MAP.get(rating_classes[1], 0)

    stock = card.select_one("p.availability").get_text(strip=True)
    link = urljoin(page_url, card.h3.a["href"])  # ubah link relatif jadi link penuh

    return {"title": title, "price_gbp": price, "rating": rating, "stock": stock, "url": link}


def save_csv(books, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(books)


def main():
    books = []
    for number in range(1, PAGES + 1):
        url = BASE_URL.format(number)
        print(f"Fetching page {number}: {url}")
        soup = fetch_page(url)
        for card in soup.select("article.product_pod"):
            books.append(parse_book(card, url))
        time.sleep(DELAY_SECONDS)

    save_csv(books, "books.csv")
    print(f"Done! {len(books)} books saved to books.csv")

    cheapest = min(books, key=lambda b: b["price_gbp"])
    average = sum(b["price_gbp"] for b in books) / len(books)
    print(f"Cheapest book: {cheapest['title']} (GBP {cheapest['price_gbp']})")
    print(f"Average price: GBP {average:.2f}")


if __name__ == "__main__":
    main()

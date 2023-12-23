# Mango Women's Category Web Scraping  
## Overview

This Python script set scrapes product details from Mango's "women" category. It involves two steps:

1. **Product Name and Genre Scraper (`product_name_and_genre_scraper.py`):**
   - Gathers product names and genres from various "women" clothing categories.
   - Saves results in `product_data.json`.

2. **Clothing Info Scraper (`clothing_info_scraper.py`):**
   - Extracts detailed information for each product using `product_data.json`.
   - Saves results in `output.json`.

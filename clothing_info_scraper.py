from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import time

def process(product_data,page,json_file):
    max_retries = 3
    current_retry = 0
    scraped=False
    while not(scraped) and current_retry<max_retries:
        global i
        for idx, product in enumerate(product_data["products"][i:]):
            print(f"Visiting product: {product['name']}")
            print(f"description link : https://shop.mango.com{product['href']}")
            description_link = "https://shop.mango.com" + product['href']
            while not(scraped) :
                try:
                    page.goto(f"https://shop.mango.com{product['href']}")
                    break
                except:
                     print(f"failed to go to the page of {product['href']} due network delays we will try again")
                     current_retry+=1
                     time.sleep(2)
            
            page.wait_for_load_state("load")

            page.wait_for_selector("#renderedImages")
            rendered_images_content = page.inner_html("#renderedImages")
            list_images = []

            ul_elements = page.query_selector_all("#renderedImages ul")
            for ul_element in ul_elements:
                img_elements = ul_element.query_selector_all("img")
                for img_element in img_elements:
                    img_src = img_element.get_attribute("src")
                    list_images.append(img_src)

            list_images = list(set(list_images))
            print(f"Images : {list_images}")
            print(len(list_images))

            # Extracting description
            page.wait_for_selector("#productDesktop > main > div > div.product-info > div.product-info-wrapper > div:nth-child(1) > p")
            description_element = page.evaluate('el => el.textContent', page.query_selector("#productDesktop > main > div > div.product-info > div.product-info-wrapper > div:nth-child(1) > p"))
            print("Description: ", description_element)

            # Extracting prices
            try:
                 actual_price = page.inner_html("#productDesktop > main > div > div.product-actions > div.product-features-prices > div.price-wrapper > div > div.ezes7.kBC9T > span:nth-child(4) > span > span").replace("QAR ", "").strip()
                 previous_price = page.inner_html("#productDesktop > main > div > div.product-actions > div.product-features-prices > div.price-wrapper > div > div.ezes7.kBC9T > span:nth-child(2) > span > span").replace("QAR ", "").strip()
                 print("previous_price : ",previous_price) 
            except:
                 actual_price = page.inner_html("#productDesktop > main > div > div.product-actions > div.product-features-prices > div.price-wrapper > div > div > span.KFpIt > span > span").replace("QAR ", "").strip()
                 previous_price=actual_price

            print("actual_price: ",actual_price)

            # Extracting colors
            colors_list = page.query_selector_all("#colorsContainer div")
            list_colors = [color.get_attribute("aria-label").replace(" selected ", "").strip().replace(" selected", "").strip() for color in colors_list]
            print("Colors: ", list_colors)

            # Extracting available sizes
            list_size = page.query_selector_all("#sizesContainer > div > ul li")
            list_size_available = [li.query_selector('button[data-testid="pdp.sizeSelector.size.available"]').text_content().replace("Last few items!", "").strip() for li in list_size if li.query_selector('button[data-testid="pdp.sizeSelector.size.available"]')]
            print("Available Sizes: ", list_size_available)

            # Create the current product's element_json
            element_json = {
                "date_web_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "brand": "Mango",
                "gender": "women",
                "category": product['genre'],
                "product_name": product['name'],
                "colors": list_colors,
                "description": description_element,
                "description_link": description_link,
                "possible_sizes": list_size_available,
                "images": list_images,
                "actual_price": actual_price,
                "previous_price": previous_price
            }

            # Write the current element_json to output.json
            json.dump(element_json, json_file, indent=2)
            i+=1
            # Add a comma and newline if it's not the last product
            if idx < len(product_data["products"]) - 1:
                json_file.write(",\n")
                print("indice : ",i)
        scraped=True

           

            

with sync_playwright() as p:
    browser = p.firefox.launch()
    context = browser.new_context()
    page = context.new_page()

    # Load the product data from the JSON file
    with open("product_data.json", "r") as json_file:
        product_data = json.load(json_file)

    # Open output.json for writing
    with open("outputfinalaktharmen199.json", "w") as json_file:
        json_file.write("[\n")  # Start the list
        print("number of lines we have to precess is : ",len(product_data["products"]))
        i = 0
        while i<len(product_data["products"]):
             try:
                process(product_data,page,json_file)
             except:
                print("we will try again")
        



        json_file.write("\n]")  # End the list

    browser.close()
    print("done")





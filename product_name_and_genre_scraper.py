from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

with sync_playwright() as p:
    browser = p.firefox.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://shop.mango.com/qa-en")
    page.click("#vsv-mm-she")
    page.wait_for_load_state("load")
    clothing_she_content = page.inner_html("#vsv-urlsmenu-she > div.vsv-lists.vsv-lists-IN > div:nth-child(1) > ul")
    product_data = {
        "products": []
    }
    list_nbProducts={}
    soup = BeautifulSoup(clothing_she_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        print("content:", link.text.strip())
        print("Link:", link['href'])
        print(f"link to go is : https://shop.mango.com{link['href']}")
        page.goto(f"https://shop.mango.com{link['href']}")
        page.wait_for_load_state("load")
        print(page.url)
        try:
            page.click("#navColumns4", force=True)
            page.wait_for_load_state("load")
            page.click('button:has-text("4")', force=True)
            page.wait_for_load_state("load")
            click_result = page.wait_for_event("click")
            page.wait_for_load_state("load")
            print(f"Click result: {click_result}")
        except:
            None
        product_selector = '[id^="product-key-id-"]'
        print("en cours")
        product_elements = page.query_selector_all(product_selector)
        nbProducts=len(product_elements)
        list_nbProducts[link.text.strip()]=nbProducts
        print(f"Number of products: {nbProducts}")
        for i, product_element in enumerate(product_elements):
            product_content = page.evaluate('(element) => element.outerHTML', product_element)
            name = page.evaluate('(element) => element.querySelector(".product-name").textContent', product_element)
            href = page.evaluate('(element) => element.querySelector("a").getAttribute("href")', product_element)
            product_data["products"].append({"genre":link.text.strip(),"name":name,"href":href})
        print("------------------")
    with open("product_data.json", "w") as json_file:
            json.dump(product_data, json_file, indent=2)
    with open("list_nbProducts.json", "w") as json_file:
         json.dump(list_nbProducts, json_file, indent=2)
    browser.close()
    print("done")

import hashlib as hsh
import json as js

from scrapers import paloaltonetworks

if __name__ == "__main__":
    # Read links
    with open("./domains/0-paloaltonetworks-86.txt", "r") as file:
        links = file.read().splitlines()

    # Master dictionary to store all data
    master = {}

    # Iterate each link and get the data
    for i, link in enumerate(links):
        print("Scraping link", i + 1, "-> ", end="")

        data = paloaltonetworks(link)

        # Check if the returned dict is empty
        if len(data.keys()) != 0:
            # Save scraped data from current link to master dict
            master[hsh.sha1(link.encode()).hexdigest()] = data

    # Write to disk
    with open(".\\scraped.json", "w", encoding="utf-8") as f:
        js.dump(master, f)

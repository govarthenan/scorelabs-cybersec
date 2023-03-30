import requests as req
from bs4 import BeautifulSoup as bs

"""Scrape given link and return in the below dict format, unless otherwise specified."""
return_format = {
    "title": "Actual title",
    "text": [
        {"type": "para", "contents": ["blah blah blah"]},
        {"type": "caption", "contents": ["clah clah clah"]},
    ],
}

# Set appropriate request headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/109.0.0.0 Safari/537.36"
}


def paloaltonetworks(link: str) -> dict:
    # Placeholders
    data = {"title": None, "text": []}

    # Fetch html and parse it
    raw = req.get(
        link,
        headers=headers,
    )
    soup = bs(raw.content, "lxml")

    # Detect if the link is a Research Report (PDF),and skip the link
    # See if there's the Resource Header class, which should indicate if it's a download page
    if soup.body.find("h1", class_="resource-heading h2".split()) is not None:
        print(f"Skipping ({soup.title.text.strip()}) as it's a research PDF.")
        return {}

    # Title
    # Try to get title from BS4 object
    title = soup.title.text.strip()
    if len(title) != 0:
        data["title"] = title
    else:
        # Get title using classic search method
        title_tag = soup.body.find(
            "h1", class_="article__header__title mb-sm-30 mb-40".split()
        )
        data["title"] = title_tag.text.strip()

    # Aesthetic
    print(data["title"])

    # Select article container tag
    article_container = soup.body.find(
        "div", class_="article__content pb-30 at-element-marker".split()
    )

    # Loop through the container
    # Append texts and captions
    for child in article_container.children:
        if str(type(child)) == "<class 'bs4.element.Tag'>":

            if child.name == "p":
                # Check for the translation tag
                if (
                    child.attrs.get("class")
                    == "wpml-ls-statics-post_translations wpml-ls".split()
                ):
                    continue

                # Check for empty p tags
                if len(child.text.strip()) == 0:
                    continue

                # Check for image captions
                # If a p tag contains image captions, add the caption to corresponding array
                if "em" in [
                    x.name
                    for x in child.children
                    if str(type(x)) == "<class 'bs4.element.Tag'>"
                ]:
                    data["text"].append(
                        {
                            "type": "caption",
                            "content": [child.text.strip()],
                        }
                    )
                    continue

                # If none of the above condition were met, then the p tag most probably contains text
                data["text"].append(
                    {
                        "type": "paragraph",
                        "content": [
                            child.text.encode("ascii", "ignore").decode("utf-8").strip()
                        ],
                    }
                )

    return data

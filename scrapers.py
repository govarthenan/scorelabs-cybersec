import requests as req
from bs4 import BeautifulSoup as bs

# Set appropriate request headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/109.0.0.0 Safari/537.36"
}


def paloaltonetworks(link: str) -> dict:
    # Placeholders
    data = {
        "title": None,
        "text": {"paragraphs": [], "captions": []},
    }

    # Fetch html and parse it
    raw = req.get(
        link,
        headers=headers,
    )
    soup = bs(raw.content, "lxml")

    # Get title
    # title_tag = soup.body.find(
    #     "h1", class_="article__header__title mb-sm-30 mb-40".split()
    # )
    # data["title"] = title_tag.text.strip()
    data["title"] = soup.title.text.strip()

    print('Scraping', data["title"])

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
                if len(child.text) == 0:
                    continue

                # Check for image captions
                # If a p tag contains image captions, add the caption to corresponding array
                if "em" in [
                    x.name
                    for x in child.children
                    if str(type(x)) == "<class 'bs4.element.Tag'>"
                ]:
                    data["text"]["captions"].append(
                        child.text.strip().split(".")[1].strip()
                    )
                    continue

                # If none of the above condition were met, then the p tag most probably contains text
                data["text"]["paragraphs"].append(
                    child.text.encode("ascii", "ignore").decode("utf-8").strip()
                )

    return data

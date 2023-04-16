import json as js
import spacy

# Load the model and enable relevant pipeline
nlp = spacy.load("en_core_web_lg")
nlp.disable_pipe("parser")
nlp.enable_pipe("senter")


def segment(file_path: str) -> dict:
    # Read and convert json to Python dictionary
    with open(file_path, 'r') as f:
        data = dict(js.load(f))

    segmented = {}  # Dictionary to hold segmented text

    length = len(data.keys())

    for i, page in enumerate(data.keys()):  # Iterate through each page

        segmented[page] = []  # Dict to store each page's text type and content lists

        for text in data[page]['text']:
            joined = ''.join(text['content'])  # Concatenate in case there are multiple strings

            doc = nlp(joined)
            sentences = [str(sent).strip() for sent in doc.sents]  # Save each sentence in the temporary list

            segmented[page].append({"type": text["type"], "content": sentences})  # Save in the same format

        # Aesthetic
        print('Segmented', i+1, 'out of', length)

    return segmented


if __name__ == '__main__':
    scraped_json_path = './scraped/paloaltonetworks.json'  # File path of the scraped data

    # Write to disk
    with open(f"segmented/{scraped_json_path.split('/')[-1]}", "w", encoding="utf-8") as f:
        js.dump(segment(scraped_json_path), f)

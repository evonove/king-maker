import sys
import os
import time

from lxml import etree
from selenium import webdriver


def get_comments(project_comments_url):
    # Opens project comments page
    driver = webdriver.Firefox()
    driver.get(project_comments_url)

    print("Comments loading", flush=True)
    # Get comments container and buttons to load more comments
    comments_container = driver.find_element_by_id("react-project-comments")
    load_reply = comments_container.find_elements_by_class_name("bttn-white")
    load_comments = comments_container.find_elements_by_class_name("bttn-blue")

    # Keeps loading comments until there are no more to load
    while len(load_reply) > 0 or len(load_comments) > 0:
        for button in comments_container.find_elements_by_class_name("bttn-white"):
            button.click()
        for button in comments_container.find_elements_by_class_name("bttn-blue"):
            button.click()

        # Waits loading of new comments
        time.sleep(1)

        # Gets buttons again
        load_reply = comments_container.find_elements_by_class_name("bttn-white")
        load_comments = comments_container.find_elements_by_class_name("bttn-blue")

    comments = []
    page_source = driver.page_source
    root = etree.fromstring(page_source, parser=etree.HTMLParser())
    html_comments_container = root.xpath(".//div[@id='react-project-comments']")[0]

    print("Comments loaded", flush=True)
    print("Scraping started", flush=True)
    for comment in html_comments_container.xpath(".//li"):
        is_backer = True

        # Comment is hidden skips it
        for t in comment.itertext():
            if "Show the comment." in t:
                is_backer = False
                break
        if not is_backer:
            continue

        is_superbacker = False
        is_collaborator = False
        is_creator = False
        type_spans = comment.xpath(".//span[contains(@class, 'mr1')]")
        if len(type_spans) > 0:
            author_type = type_spans[0].text
            is_superbacker = author_type == "Superbacker"
            is_collaborator = author_type == "Collaborator"
            is_creator = author_type == "Creator"

        author = comment.xpath(".//span[contains(@class, 'mr2')]")[0].text
        text = ""
        for p in comment.xpath(".//p[contains(@class, 'type-14')]"):
            if p.text:
                text += p.text
                text += "\n"
        timestamp = int(comment.xpath(".//time")[0].get("datetime"))
        comments.append(
            {
                "is_backer": is_backer,
                "is_superbacker": is_superbacker,
                "is_collaborator": is_collaborator,
                "is_creator": is_collaborator,
                "author": author,
                "text": text,
                "timestamp": timestamp,
            }
        )
        # Let's give the user a bit of feedback
        print(".", end="", flush=True)

    driver.quit()
    print()
    print("Scraping finished")
    return comments


def create_rankings(comments, output_file):
    # Dict authors -> comments list
    authors_comments = {}

    print("Saving rankings")

    for c in comments:
        author = c["author"]

        if author in authors_comments:
            authors_comments[author].append(c)
        else:
            authors_comments[author] = [c]

    # Sorts list of authors by number of comments
    authors_ranking = sorted(authors_comments.items(), key=lambda item: len(item[1]), reverse=True)

    # Writes rankings to output_file
    with open(output_file, "w") as file:
        for author in authors_ranking:
            file.write(str(len(authors_comments[author[0]])))
            file.write(" ")
            file.write(author[0])
            file.write("\n")

        # Writes longest comments of top commenters
        for author in authors_ranking[:5]:
            file.write("========================\n\n")
            file.write(f"Longest 5 comments of {author[0]}\n\n")

            author_comments = [c["text"] for c in authors_comments[author[0]]]
            author_comments.sort(key=len, reverse=True)

            # Writes longest comments
            for text in author_comments[:5]:
                file.write("------------------\n\n")
                file.write(text)
                file.write("\n\n")


if __name__ == "__main__":
    os.environ["MOZ_HEADLESS"] = "1"
    if len(sys.argv) > 2:
        print("Starting")
        create_rankings(get_comments(sys.argv[1]), sys.argv[2])
        print("Finished")
    else:
        print("Usage:")
        print("python kingmaker.py <project_comments_url> <output_file>")


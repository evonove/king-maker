import sys
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_comments(project_comments_url):
    # Opens project comments page
    driver = webdriver.Firefox()
    driver.get(project_comments_url)

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
        time.sleep(2)

        # Gets buttons again
        load_reply = comments_container.find_elements_by_class_name("bttn-white")
        load_comments = comments_container.find_elements_by_class_name("bttn-blue")

    comments = []

    for comment in comments_container.find_elements_by_tag_name("li"):
        # Comments from user that removed their pledge are hidden
        is_backer = True
        try:
            show_comment = comment.find_element_by_link_text("Show the comment.")
            show_comment.click()
            is_backer = False
        except NoSuchElementException:
            pass

        is_superbacker = False
        is_collaborator = False
        is_creator = False
        try:
            author_type = comment.find_element_by_xpath(".//span[contains(@class, 'mr1')]")
            is_superbacker = author_type == "Superbacker"
            is_collaborator = author_type == "Collaborator"
            is_creator = author_type == "Creator"
        except NoSuchElementException:
            pass

        author = comment.find_element_by_xpath(".//span[contains(@class, 'mr2')]").text
        text = comment.find_elements_by_tag_name("div")[3].text
        timestamp = int(comment.find_element_by_tag_name("time").get_attribute("datetime"))
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

    driver.quit()
    return comments


def create_rankings(comments, output_file):
    # Dict authors -> comments list
    authors_comments = {}

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
        create_rankings(get_comments(sys.argv[1]), sys.argv[2])
    else:
        print("Usage:")
        print("python kingmaker.py <project_comments_url> <output_file>")


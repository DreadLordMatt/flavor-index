from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub

# todo use chapter.content and read as Html, get the required css classes from that text file or read the lists into
#  csv files maybe?

# this is a list of all elements that should be excluded from processing text
blacklist =['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script']
bookPath = 'the_flavor_bible.epub' #local epub file


def read_book(epubPath):

    book = epub.read_epub(epubPath) # Path to where the ebook epub file is stored.

    chapters = [] # Open a list variable for processing each html file in the epub.

    for item in book.get_items(): # Iterate through the book for each item add it to the List as a new chapter.
        if item.get_type() == ebooklib.ITEM_DOCUMENT:   # We only want to iterate where we have Item type 9.
        # http://docs.sourcefabric.org/projects/ebooklib/en/latest/ebooklib.html
            chapters.append(item.get_content())

    return chapters     # Return a list of each chapter from the book as a sinlge html item.


def convert_chapter(chapter):   # Receives a single item from a list of HTML chapters

    output = ''     # Opens a blank string

    soup = BeautifulSoup(chapter, 'html.parser')    # Parses the HTML chapter

    text = soup.find_all(text=True)     # Returns only text elements from the HTML chapter

    for t in text:      # Iterate through the soup for each text element
        if t.parent.name not in blacklist:      # Check the tag to ensure its text
            output += '{}'.format(t)            # Format the text output as text into the string varaible

    return output       # Returns a formatted string


def ingredients(chapter):  # Accepts a single HTML chapter item

    output = {}  # Opens an empty dictionary item

    soup = BeautifulSoup(chapter, 'html.parser')  # Parse the item to return only the ingredient items

    soup
    item = soup.find_all(class_='lh1')  # Define what class and tag identifies an ingredient

    #for ingredient in ingredients:  # Find the first instance of an ingredient, iterate.

    # for t in text:
    #     if t.parent.name not in blacklist:
    #         output += '{} '.format(t)

    return output


def convert_text(thtml):    # Receives the chapters HTML list

    output = []     # Opens a list variable for all text

    for html in thtml:  # Iterate through the list of HTML chapters
        text = convert_chapter(html)    # Passing each chapter through the function, receiving only text back
        output.append(text)

    return output


def main(epubPath):

    chapters = read_book(epubPath)  # Returns a list of HTML chapters.

    ingredientList = ingredients(chapters)

    ttext = convert_text(chapters)  # Returns a formatted string of each HTML chapter combined.

    return ttext


if __name__ == "__main__":

    out = main(bookPath)
    print(out)
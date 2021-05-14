"""
Title: Flavor Bible Book Processing
Author: Matt Benoit

Description: This program reads the ebook 'The Flavor Bible' by Karen Page and Andrew
Dornenburg and processes that ebook into a database. The purpose of this, is to allow a front-
end website or application to query an ingredient, and return the corresponding flavor
affinities and other attributes.

The book categorizes the ingredients based on HTML classes lh and lh1 for each ingredient. The
flavour affinities are class ul. Strong flavor affinities follow the HTML h4 class and contain
'+' between each ingredient. Each of these strong flavour affinities include the ingredient to
which they belong.

There is a hierarchy that must be defined before this can continue. This is the relationship
between each object in the book. The book is structured to give information about what
category of culinary item can be enhanced through combination of another culinary item.

Ingredient (this really defines the class)
    Season: The ingredient's seasonal peak(s).
    Taste: The ingredient's primary taste(s), e.g. salty, sweet, bitter.
    Function: The ingredient's intrinsic property, e.g. cooling vs. warming.
    Weight: The ingredient's relative density, e.g. from light to heavy.
    Volume: The ingredient's relative flavor "loudness", e.g. from quiet to loud.
    Technique: The most commonly used techniques to prepare the ingredient.
    Tips: Suggestions for using the ingredient.
    Flavour Affinities: Compatible flavors with a rank of strength.
        Related Ingredient
        Strength
            -1  - Incompatible, Avoid
            1   - Good Pairings
            2   - Recommended by some number of experts
            3   - Highly recommended by a larger number of experts
            4   - Highly recommended "Holy Grail" by the largest number of experts
        Common Affinities: this is a list of several ingredients which are commonly used 
        together, and are well regarded.
        
Processing Summary:
    Get the list in order of appearance of all the ingredients, flavor affinities, and attributes.
    for every entry in this list identify what it is. note the category.
    
    
Hierarchy structure:
    { ingredient : ingredientDesc,
        {reference: referenceDesc},
        {season: [season]},
        {taste: [taste]},
        {function: [function]},
        {weight: []},
        {volume: []},
        {technique: []},
        {tips: []},
        {flavor_affinity : 
            {
            pairings : [{ingredient: strength}],
            affinities : []
            }
        },
    }
    
"""

from typing import Counter
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


# TODO: rename your shitty variables to ensure readability and clarity.
# TODO: Make this code OO when you refactor it.
# class Ingredient:
#     def __init__(self, name, season, taste, function, weight, volume, technique, tips, pairings, affinities):
#
#         self.name = name
#         self.season = season
#         self.taste = taste
#         self.function = function
#         self.weight = weight
#         self.volume = volume
#         self.technique = technique
#         self.tips = tips
#         self.pairings = pairings
#         self.affinities = affinities
#         self.flavour_affinity = [self.pairings, self.affinities]
#         self.details = {'season': self.season,
#                       'taste': self.taste,
#                       'function': self.function,
#                       'weight': self.weight,
#                       'volume': self.volume,
#                       'technique': self.technique,
#                       'tips': self.tips,
#                       'flavour_affinity': self.flavour_affinity}


def process_book(book_path):
    book = epub.read_epub(book_path)
    my_dict = {}
    chapters = []
    counter = 0     # Counter for the number or records we are processing.

    # This defines the contents of an "active ingredient". # TODO: remove the multiple occurrences with class
    output_dict = {'season': [], 'taste': [], 'function': [], 'weight': [], 'volume': [], 'technique': [], 'tips': [],
                   'related ingredients': [], 'flavor affinities': []}

    for i, item in enumerate(book.get_items()):  # Looks through the epub for all the items inside
        if item.get_type() == ebooklib.ITEM_DOCUMENT:  # Only process documents, ignore pictures and other junk
            chapters.append(item.get_content())  # Take each item and add it to a list

        if i == len(list(book.get_items())) - 1:
            # last_item = True
            pass

    last_chapter = False

    # TODO: Fix this garbage
    for c, chapter in enumerate(chapters[7:]):  # Iterate through each "chapter" which is a HTML file
        soup = BeautifulSoup(chapter, 'html.parser')
        # ingredient = soup.find_all('p', class_=['lh1', 'lh'])   # Get all the ingredients from the chapter html file
        child_ingredient_list = soup.find_all('p', class_=['lh1', 'lh', 'ul', 'h4'])

        if c == (len(
                chapters) - 15):  # 15 + 7 = 21 chapters in the list...fix this absolute trash. not to mention the flags
            last_chapter = True

        last_child = False
        active_ingredient = ''

        if child_ingredient_list:
            for position, child_list in enumerate(child_ingredient_list):
                # current_child = position
                current_type = child_list.attrs['class'][0]
                current_text = child_list.text

                if position == (len(child_ingredient_list) - 1):  # Are we are at the last item in the list?
                    last_child = True
                    next_type = current_type
                else:  # All other scenarios
                    next_actual_child = child_ingredient_list[position + 1]
                    next_type = next_actual_child.attrs['class'][0]

                if len(current_text.split('\r\n')) > 1:  # There are scenarios where the header contains multiple
                    # primary ingredients. for these scenarios we need to split them at the new line indicator,
                    # and process each.
                    temp_list = current_text.split('\r\n')
                    for t, temp in enumerate(temp_list):
                        if t == len(temp_list) - 1:  # if we are at the last item in the temp_list break and proceed
                            active_ingredient = temp.strip()
                            break
                        else:
                            my_dict[temp.strip()] = output_dict.copy()  # Write the blank entry
                            output_dict.clear()
                            counter += 1
                            output_dict = {'season': [], 'taste': [], 'function': [], 'weight': [], 'volume': [],
                                           'technique': [],
                                           'tips': [], 'related ingredients': [], 'flavor affinities': []}
                elif current_type in ['lh', 'lh1']:  # if the current item is a header set the active ingredient
                    active_ingredient = child_list.text

                if " + " in current_text:
                    output_dict['flavor affinities'].append(current_text)
                elif "Season:" in current_text:
                    output_dict['season'].append(current_text.replace("Season: ", ""))
                elif "Taste:" in current_text:
                    output_dict['taste'].append(current_text.replace("Taste: ", ""))
                elif "Function:" in current_text:
                    output_dict['function'].append(current_text.replace("Function: ", ""))
                elif "Weight:" in current_text:
                    output_dict['weight'].append(current_text.replace("Weight: ", ""))
                elif "Volume:" in current_text:
                    output_dict['volume'].append(current_text.replace("Volume: ", ""))
                elif "Techniques:" in current_text:
                    output_dict['technique'].append(current_text.replace("Techniques: ", ""))
                elif "Tips:" in current_text:
                    output_dict['tips'].append(current_text.replace("Tips: ", ""))
                elif current_type == 'ul':  # This is the primary iterator action adding ingredients to the list
                    # TODO: Add processing here to determine the strength of the relationship. this will require a new
                    #  dictionary. Strength ratings are shown in the header (-1, 1, 2, 3, 4).
                    output_dict['related ingredients'].append(child_list)
                    
                # When the iteration encounters something that isn't an ingredient, like a new active ingredient
                # it must decide what happens. This is identified by the HTML Class, and the style of the text.
                if current_type in ['lh1', 'lh'] and next_type in ['lh1', 'lh']:
                    # If it is currently a header, and the next value is going to be a header, write the entry
                    my_dict[active_ingredient] = output_dict.copy()
                    output_dict.clear()
                    counter += 1
                    output_dict = {'season': [], 'taste': [], 'function': [], 'weight': [], 'volume': [],
                                   'technique': [],
                                   'tips': [], 'related ingredients': [], 'flavor affinities': []}
                elif current_type == 'ul' and next_type in ['lh1', 'lh']:
                    # If the next item is a header, write the entry
                    my_dict[active_ingredient] = output_dict.copy()
                    output_dict.clear()
                    counter += 1
                    output_dict = {'season': [], 'taste': [], 'function': [], 'weight': [], 'volume': [],
                                   'technique': [],
                                   'tips': [], 'related ingredients': [], 'flavor affinities': []}
                elif last_child is True and last_chapter is True:
                    # If this is the last item in the chapters list and the last child in the children list, finish.
                    my_dict[active_ingredient] = output_dict.copy()
                    output_dict.clear()
                    counter += 1
                    output_dict = {'season': [], 'taste': [], 'function': [], 'weight': [], 'volume': [],
                                   'technique': [],
                                   'tips': [], 'related ingredients': [], 'flavor affinities': []}
                
    return my_dict


def output_data(dictionary_object):
    # Write the output to a file
    # TODO: change the output to JSON so we can use this to generate a mongo insert statement
    # TODO: get an ERD for the mongo DB sorted out before you start crafting any inserts. ensure you have direction
    file_name = 'list.txt'
    t = open(file_name, "w")
    t.truncate()
    t.write(str(dictionary_object))
    t.close()
    print("Data written to file: {}".format(file_name))


if __name__ == '__main__':

    output = process_book('the_flavor_bible.epub')
    output_data(output)

# Flavor Index and Relationships
The objective of this project is to digitize one of my favourite culinary books "The Flavor Bible" by Karen Page and Andrew Dornenburg. The book is excellent and gives insight into improving creativity, enhanceing the eating expierence and impact of a dish. Page and Dornenburg have provided readers with a thorough tool which can be used as a reference while cooking. The book contains some 500 charts, describing the relationship between an ingredient, cuisine, flavor, and taste.

Over the last 5 years I've used this book countless times, and finally relented to the nagging voice in my head. The primary issue I've identified is flipping between multiple ingredients as a build out a dish. To combat this, I've presented the book as a web page with search functionality.

## Credits:
If you like this idea and want to learn more about the book, please support the authors and pick up a copy. They can be purchased from [Amazon](https://www.amazon.ca/gp/product/0316118400/ref=dbs_a_def_rwt_bibl_vppi_i0) or direct [from the authors](https://karenandandrew.com/books/the-flavor-bible/).

## PY Processing of ebook
Using a epub of the book we can strip the required text and process with a short python script. Once the data is cleaned and organized it can be passed to a front end web app for presentation. The is built in Vue.js and allows each ingredient to be retrieved, and presented via search in a text box, or via an alphabet line. 

# Next Steps
Future Functionality:
* Based on the flavor relation weight matrix groups of ingredients can be entered in a list and an overall score calculated
* Web recipes can be passed from jackcooks.ca to evaluate them and give a score
* Suggestions for added ingredients based on a recipe or list, to improve the score
* Relationship graphing: social graphs can be modeled, showing the relationship, and ingredient families
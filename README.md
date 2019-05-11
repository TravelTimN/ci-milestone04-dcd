# 2BN-Desserts

_TBD_

---

## Table of Contents
1. [**UX**](#ux)
    - [**User Stories**](#user-stories)
    - [**Design**](#design)
        - [**Framework**](#framework)
        - [**Color Scheme**](#color-scheme)
        - [**Typography**](#typography)
    - [**Wireframes**](#wireframes)

2. [**Features**](#features)
    - [**Existing Features**](#existing-features)
    - [**Features Left to Implement**](#features-left-to-implement)

3. [**Technologies Used**](#technologies-used)
    - [**Front-End Technologies**](#front-end-technologies)
    - [**Back-End Technologies**](#back-end-technologies)

4. [**Testing**](#testing)
    - [**Automated Testing**](#automated-testing)
    - [**Manual Testing**](#manual-testing)
    - [**Validators**](#validators)
    - [**Compatibility**](#compatibility)

5. [**Deployment**](#deployment)
    - [**Local Deployment**](#local-deployment)
    - [**Remote Deployment**](#remote-deployment)

6. [**Credits**](#credits)
    - [**Content**](#content)
    - [**Media**](#media)
    - [**Code**](#code)
    - [**Acknowledgements**](#acknowledgements)

---

## UX

_TBD_

### User Stories

"**_As a user, I would like to_** _____________________________"

- *view the site* from **any device** *(mobile, tablet, desktop)*.
- *view all recipes* as a **Guest**. :white_check_mark:
- *filter recipes* by **dessert type**. :white_check_mark:
- *filter recipes* by **author**. :white_check_mark:
- *filter recipes* by **allergen**. :white_check_mark:
- *sort/order recipes* by **author, favorites, last updated, recipe name, total time, and views**. :white_check_mark:
- **limit** the number of *recipes* to display, or see *all recipes*. :white_check_mark:
- *create* my **own profile**. :white_check_mark:
- *add* my **own recipes**. :white_check_mark:
- *edit* my **own recipes**. :white_check_mark:
- *delete* my **own recipes**. :white_check_mark:
- be able to **log out**. :white_check_mark:
- *save recipes* in **my favorites**. :white_check_mark:
- *remove recipes* from **my favorites**. :white_check_mark:
- *see instructions* on how to **add a recipe**.
- **print** a *particular recipe*.
- *see* **recommended recipes** after *viewing a recipe*.
- *see* the **total views** of *a recipe*. :white_check_mark:
- *see* how many people **like** my *recipes*. :white_check_mark:
- *see* a cooking/baking **conversion table**.

### Design

_TBD_

#### Framework

- [Materialize 1.0.0](https://materializecss.com/)
    - I really like the modern and clean layout of Materialize as a framework, with its simple-to-understand documentation.
- [jQuery 3.4.0](https://code.jquery.com/jquery/)
    - _tbd_ (javascript framework)
- [Flask 1.0.2](http://flask.pocoo.org/)
    - _tbd_ (microframework)

#### Color Scheme

_TBD_

#### Typography

- [Materialize Icons](https://materializecss.com/icons.html)
    - I've retained some of the standard Materialize Icons that are used in certain components.
- [Font Awesome 5.8.1](https://fontawesome.com/)
    - Although Materialize Icons have nearly 1,000 free-to-use icons, I prefer the look of Font Awesome's icons, and they have more to suit my specific needs for this project.

### Wireframes

_TBD_

##### back to [top](#table-of-contents)

---

## Features

**Register Account**
- _TBD_ (Authentication & Authorization)

**Log In to Account**
- _TBD_ (Authentication & Authorization)

**Log Out of Account**
- _TBD_

**View All Desserts**
- _TBD_

**Search Desserts**
- _TBD_

**Add a Recipe**
- _TBD_ (C in Crud)

**View a Recipe**
- _TBD_ (R in cRud)

**Update a Recipe**
- _TBD_ (U in crUd)

**Delete a Recipe**
- _TBD_ (D in cruD)

**Save a Recipe to Favorites**
- _TBD_

**Remove a Recipe from Favorites**
- _TBD_
 
### Existing Features

_TBD_

### Features Left to Implement

_TBD_

##### back to [top](#table-of-contents)

---

## Technologies Used

- [VS Code](https://code.visualstudio.com/) - (ide)
- [GitHub](https://github.com/) - (remote storage of code)
- [Photoshop CS6](https://www.adobe.com/Photoshop) - (image editing)

### Front-End Technologies

- [HTML](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) - (markup text)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3) - (cascading styles)
- [jQuery 3.4.0](https://code.jquery.com/jquery/) - (javascript framework)
- [Materialize 1.0.0](https://materializecss.com/) - (design framework)


### Back-End Technologies

- **Flask**
    - [Flask 1.0.2](http://flask.pocoo.org/) - (microframework)
    - [Jinja 2.10](http://jinja.pocoo.org/docs/2.10/) - (templating)
    - [Werkzeug 0.14](https://werkzeug.palletsprojects.com/en/0.14.x/) - (login + password hashing)
- **Heroku**
    - [Heroku](https://www.heroku.com) - (app hosting)
- **Python**    
    - [Python 3.6.7](https://www.python.org/) - (back-end programming language)
    - [MongoDB Atlas](https://www.mongodb.com/) - (cloud database)
    - [PyMongo 3.8.0](https://api.mongodb.com/python/current/) - (python api for mongodb)
    - [Python Slugify 3.0.2](https://pypi.org/project/python-slugify/) - (user-friendly url)

##### back to [top](#table-of-contents)

---

## Testing

_TBD_

### Automated Testing

_TBD_

### Manual Testing

**Pagination**

When implementing pagination, I had a lot of manual tests to undergo, in order to make pagination work for multiple scenarios. I needed to test that all aspects of pagination worked with and without the option for searching the database. These included:

- **Pagination without Search**
    - Pagination works if no URL args present on initial load.
    - *Previous Page* button disabled on first page of all recipes shown.
    - *Next Page* button disabled on last page of all recipes shown.
    - Appropriate number of pages appear based on the initial 12 items per page with correct number of recipes in database.
    - Additional page numbers appear if more recipes are added.
    - Each page number returns their correct page URL.

- **Pagination with Search**
    - Pagination works if no URL args present on initial search.
    - No pagination shown if 0 search results.
    - No pagination shown if only 1 page of search results.
    - No pagination shown if fewer results than user-selected items per page.
    - No pagination shown if user selects *All* results to be displayed.
    - *Previous Page* button disabled on first page of multi-page search results.
    - *Next Page* button disabled on last page of multi-page search results.
    - Appropriate number of pages appear based on user-selected items per page.
    - Additional page numbers appear if more recipes are added.
    - Each page number returns their correct page URL.

**Sort, Order, and Limit**

With the Search function, the user has the option to sort, order, and limit the number of results. This required some manual testing as well.

- **Sorting + Ordering**
    - Sorting by *Author* or *Recipe Name* works accordingly:
        - ascending (alphabetical A-Z)
        - descending (alphabetical Z-A)
    - Sorting by *Favorites* or *Views* works accordingly:
        - ascending (lowest to highest)
        - descending (highest to lowest)
    - Sorting by *Last Edited* works accordingly:
        - ascending (oldest to newest)
        - descending (newest to oldest)
    - Sorting by *Total Time* works accordingly:
        - ascending (shortest to longest)
        - descending (longest to shortest)

- **Limiting**
    - Limit results by 8 | 12 | 16 | 20 recipes per page:
        - Depending on number of results found, correct pagination for user-selected number of items to display.
    - Show *All* results on single page:
        - No matter how many results are found, if user selects *All*, it will show all results on a single page without Pagination.

### Validators

_TBD_

### Compatibility

_TBD_

##### back to [top](#table-of-contents)

---

## Deployment

_TBD_

### Local Deployment

_TBD_

### Remote Deployment

_TBD_

##### back to [top](#table-of-contents)

---

## Credits

### Content

- [*"How to Write a Git Commit Message"*](https://chris.beams.io/posts/git-commit/) by **Chris Beams** (*as recommended by Code Institute assessors on previous projects*)

### Media

Sources of the images used on this site:

- **favicon** : [Clipart-Library](http://clipart-library.com/kawaii-cookie-cliparts.html)
- **recipe placeholder image** : [Pixabay](https://pixabay.com/photos/waffles-waffles-bake-ingredients-2190961/)
- **profile avatars** : [123rf](https://www.123rf.com/photo_40610865_stock-vector-cute-kawaii-dessert-cake-macaroon-ice-cream-icons.html)

### Code

- Suggested **.gitignore** files from [GitHub/gitignore](https://github.com/github/gitignore)

- **Custom Toast** on *page load* (instead of **Materialize Toasts** with an *onclick* event) for my Flask Flash Messages: [StackOverflow](https://stackoverflow.com/questions/43345678/how-to-display-the-snack-bar-on-page-load)

- **Custom list item** attributes (instead of standard bullet points) for my recipe *Directions*: [CSS Tricks](https://css-tricks.com/custom-list-number-styling/)

### Acknowledgements

- [Ignatius Ukwuoma](https://github.com/ignatiusukwuoma)
    - My Code Institute mentor.
- [Chris Quinn](https://github.com/10xOXR)
    - My accountability partner on all projects.
- [Sean Murphy](https://github.com/nazarja)
    - For helping me have a euphoric epiphany on how things work with the back-end.

##### back to [top](#table-of-contents)
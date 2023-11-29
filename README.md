# Commerce
## Demo
[![demo](https://github.com/jim37500/commerce/blob/main/commerce%20demo.png)](https://www.youtube.com/watch?v=NXjOq8zKM_k)
## Getting Started
- In your terminal, cd into the commerce directory.
- Run python manage.py makemigrations auctions to make migrations for the auctions app.
- Run python manage.py migrate to apply migrations to your database.

## Specification
### Models 
- Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
### Create Listing
- Users will be able to visit a page to create a new listing. They will be able to specify a title for the listing, a text-based description, and what the starting bid will be. Users will also optionally be able to provide a URL for an image for the listing and/or a category.
### Active Listings Page 
- The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page will display (at minimum) the title, description, current price, and photo (if one exists for the listing).
### Listing Page 
Clicking on a listing will take users to a page specific to that listing. On that page, users will be able to view all details about the listing, including the current price for the listing.
- If the user is signed in, the user will be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user will be able to remove it.
- If the user is signed in, the user will be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user will be presented with an error.
- If the user is signed in and is the one who created the listing, the user will have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
- If a user is signed in on a closed listing page, and the user has won that auction, the page will say so.
- Users who are signed in 2ill be able to add comments to the listing page. The listing page will display all comments that have been made on the listing.
### Watchlist
- Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
### Categories
- Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

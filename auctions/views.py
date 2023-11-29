from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import NewListingForm, NewBidForm
from django.db.models import Count
from .models import User, Listing, Bid, Comment
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            img_url = form.cleaned_data['img_url']
            category = form.cleaned_data['category']
            price = form.cleaned_data['starting_bid']
            description = form.cleaned_data['description']

            # Create and save an instance of the model
            instance = Listing(title=title, img_url=img_url, category=category, user=request.user,price=price, description=description)
            instance.save()
        
        return HttpResponseRedirect(reverse("index"))
    

    else:
        form = NewListingForm()
        return render(request, "auctions/create.html", {
            'form': form
        })
    

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    is_in_watchlist = False
    is_active = listing.is_active
    is_seller = False

    if request.user.is_authenticated:
        if listing in request.user.watch_list.all():
            is_in_watchlist = True
        if request.user == listing.user:
            is_seller = True
    comments = Comment.objects.filter(product_id=listing_id)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = NewBidForm(request.POST)
            if form.is_valid():
                # Process the form data
                price = form.cleaned_data["price"]
                current_price = listing.price
                message = ""
                if price > current_price:
                    update_bid = Bid(user = request.user, price=price, product_id=listing_id)
                    update_bid.save()
                    current_price = price
                    listing.price = current_price
                    listing.save()
                    message = "Successfully bidden"
                else:
                    message = "The bid price must larger than current price"
                
                bid_price = f"${current_price:.2f}"
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_price": bid_price,
                    "form": form,
                    "message": message,
                    "is_in_watchlist": is_in_watchlist,
                    "is_seller": is_seller,
                    "is_active": is_active,
                    "comments": comments
                })
        else:
            return HttpResponseRedirect('/login')
    else:
        listing_price = listing.price
        bid_price = f"${listing_price:.2f}"
        form = NewBidForm()
        try:
            bid = Bid.objects.get(price=listing_price)
            winner = bid.user
            winner_alert = False
            if request.user.is_authenticated and request.user == winner:
                winner_alert = True
        except ObjectDoesNotExist:
            bid = None
            winner = ""
            winner_alert = False

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_price": bid_price,
            "form": form,
            "is_in_watchlist": is_in_watchlist,
            "is_seller": is_seller,
            "is_active": is_active,
            "winner": winner,
            "winner_alert": winner_alert,
            "comments": comments
        })
    

@login_required
def manage_watchlist(request):
    listing_id = request.POST.get('listing_id')
    listing = Listing.objects.get(id=listing_id)
    if listing in request.user.watch_list.all():
        request.user.watch_list.remove(listing)
    else:
        request.user.watch_list.add(listing)
    
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))



@login_required
def view_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watch_list.all()
    })


@login_required
def close_listing(request):
    listing_id = request.POST.get('listing_id')
    listing = Listing.objects.get(id=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def leave_comment(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        content = request.POST.get('content')
        new_comment = Comment(user=request.user, content=content, product_id=listing_id)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def category(request):
    listings_by_category = Listing.objects.values('category').annotate(total_listings=Count('category'))
    return render(request, "auctions/categories.html", {
        "categories": listings_by_category
    })

def filter(request, category_name):
    return render(request, "auctions/filter.html", {
        "listings": Listing.objects.filter(category=category_name),
        "category": category_name
    })
    

        
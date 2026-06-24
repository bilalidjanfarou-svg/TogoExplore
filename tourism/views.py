from django.shortcuts import render, get_object_or_404, redirect
from .models import TouristSite, Category
from .models import TouristSite, Category, Review
from django.contrib.auth.decorators import login_required
from .models import Favorite





def home(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    sites = TouristSite.objects.all()

    if query:
        sites = sites.filter(name__icontains=query)

    if category_id:
        sites = sites.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'sites': sites,
        'categories': categories
    }

    return render(request, 'tourism/index.html', context)


def site_detail(request, id):

    site = get_object_or_404(TouristSite, id=id)

    if request.method == 'POST':

        author = request.user.username
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        Review.objects.create(
            site=site,
            author=author,
            comment=comment,
            rating=rating
        )

    context = {
        'site': site
    }

    return render(request, 'tourism/site_detail.html', context)


def contact(request):

    return render(request, 'tourism/contact.html')

@login_required
def delete_review(request, review_id):

    review = get_object_or_404(Review, id=review_id)

    if review.author == request.user.username:
        site_id = review.site.id
        review.delete()
        return redirect('site_detail', id=site_id)
    
    return redirect('home')


@login_required
def add_favorite(request, site_id):

    site = get_object_or_404(TouristSite, id=site_id)

    Favorite.objects.get_or_create(
        user=request.user,
        site=site
    )
                             

    return redirect('site_detail', id=site.id)

@login_required
def favorites(request):

    favorites= Favorite.objects.filter(
        user=request.user
    )

    return render(
        request,
        'tourism/favorites.html',
        {'favorites': favorites}
    )















































































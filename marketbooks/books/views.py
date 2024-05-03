
from django.http import HttpResponse
from django.template import loader
from .models import Book, BooksCategory, Customer, Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.http import HttpResponseServerError


from django.views import View
from .forms import CustomerRegistrationForm, CustomerprofileForm
from django.contrib import messages

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def wishlist(request):
    # Assuming the user is logged in and you have access to the customer object
    customer = Customer.objects.get(user=request.user)  # Assuming you have a User object in the request
    wishlist_books = customer.wishlist.all()
    return render(request, 'wishlist.html', {'wishlist_books': wishlist_books})

def add_to_wishlist(request, slug):
    book = get_object_or_404(Book, slug=slug)
    customer = Customer.objects.get(user=request.user)  
    # Add the book to the wishlist
    customer.wishlist.add(book)
    return redirect('/wishlist') 

def remove_from_wishlist(request, slug):
    book = get_object_or_404(Book, slug=slug)
    customer = Customer.objects.get(user=request.user) 
    # Remove the book from the wishlist
    customer.wishlist.remove(book)
    return redirect('/wishlist') 



def Homepage(request):
    books = Book.objects.order_by('-created_at')[:8]
    recommended_books = Book.get_recommended_books()
    must_read_books = Book.get_must_read_books()

    context = {
        'books': books,
        'recommended_books': recommended_books,
        'must_read_books': must_read_books
    }
    return render(request, 'index.html', context)

def search_results(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query)
    authors = Author.objects.filter(name__icontains=query)
    context = {'books': books, 'authors': authors, 'query': query}
    return render(request, 'search_results.html', context)



@login_required
def product_detail(request, slug):
    try:
        book = get_object_or_404(Book, slug=slug)

        host = request.get_host()

        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': book.price,
            'item_name': book.title,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}/payment-success/{book.slug}/",
            'cancel_url': f"http://{host}/payment-failed/{book.slug}/",

        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context = {
            'book': book,
            'paypal': paypal_payment
        }

        return render(request, 'product-single.html', context)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in product_detail view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")


def PaymentSuccessful(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, 'payment-success.html', {'book': book})

def paymentFailed(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, 'payment-failed.html', {'book': book})



@login_required
def download_book(request, slug):
    try:
        book = get_object_or_404(Book, slug=slug)
        file_path = book.file.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=' + book.file.name.split('/')[-1]
            return response

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in product_detail view: {e}")
        # Return a server error response
        return HttpResponseServerError("Sorry, something went wrong. Please try again later.")


def Shop(request, category_id=None):
    books = Book.objects.all()
    categories = BooksCategory.objects.all()
    
    # Filter books by category if a category ID is provided
    if category_id:
        category = get_object_or_404(BooksCategory, id=category_id)
        books = books.filter(category=category)
   
   
    page = Paginator(books, 21)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    #Filter books based on price range if the form is submitted
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        print("Min Price:", min_price)
        print("Max Price:", max_price)
        books = Book.filter_by_price_range(min_price, max_price)
        print("Filtered Books Count:", books.count())

    return render(request, 'shop.html',
                  {
                      'page': page,
                       'categories': categories,
                        'min_price': min_price,  # Pass back the min_price and max_price for form persistence
                        'max_price': max_price,
                   }
                  )


# def Category_book(request, category_id):
#     category = get_object_or_404(BooksCategory, pk=category_id)
#     books = Book.objects.filter(category=category)
#     return render(request, 'shop.html', {'category': category, 'books': books})




class CustomRegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = CustomerRegistrationForm()
        return render(request, 'register.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation! User Registration was  successfully.")

        else:
            messages.error(request, "Invalid cridentials please try again")
        return render(request, 'register.html', locals())


class ProfileView(View):

    def get(self,request):
        form = CustomerprofileForm()
        return render(request, 'profile.html', locals())
    def post(self,request):
        form = CustomerprofileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']


            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation! profile was  successfully saved.")
        else:
            messages.error(request, "Invalid cridentials please try again")

        return render(request, 'profile.html', locals())


@login_required
def Address(request):
    try:
        add = Customer.objects.filter(user=request.user)
        return render(request, 'address.html', locals())

    except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error in product_detail view: {e}")
            # Return a server error response
            return HttpResponseServerError("Sorry, something went wrong. Please try again later.")



def logout_view(request):
    logout(request)
    return redirect('/')












def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def blog(request):
    template = loader.get_template('blog.html')
    return HttpResponse(template.render())

def blogSingle(request):
    template = loader.get_template('blog-single.html')
    return HttpResponse(template.render())

def Cart(request):
    template = loader.get_template('cart.html')
    return HttpResponse(template.render())

def Checkout(request):
    template = loader.get_template('checkout.html')
    return HttpResponse(template.render())


# def ProductSingle(request):
#     template = loader.get_template('product-single.html')
#     return HttpResponse(template.render())
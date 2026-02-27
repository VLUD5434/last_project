from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import logout

from .models import Game, Cart, Library, LibraryGame

User = get_user_model()


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'store/login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Паролі не співпадають")
            return render(request, 'auth/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Такий логін уже зайнятий")
            return render(request, 'store/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Такий email уже використовується")
            return render(request, 'store/signup.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Акаунт створено! Тепер увійдіть.")
        return redirect('login')

    return render(request, 'store/signup.html')


@login_required
def home(request):
    query = request.GET.get("q", "")

    games = Game.objects.all().order_by("title")

    if query:
        games = games.filter(
            Q(title__icontains=query) |
            Q(genre__icontains=query)
        )

    paginator = Paginator(games, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    cart_count = 0
    if hasattr(request.user, "cart"):
        cart_count = request.user.cart.games.count()

    return render(request, "store/home.html", {
        "page_obj": page_obj,
        "cart_count": cart_count,
        "query": query,
    })


@login_required
def theme_toggle(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    request.user.dark_background = not request.user.dark_background
    request.user.save()

    return JsonResponse({
        "dark": request.user.dark_background
    })


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'store/game_detail.html', {'game': game})


@login_required
def add_to_cart(request, game_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    game = get_object_or_404(Game, id=game_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.games.add(game)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "message": "added",
            "cart_count": cart.games.count()
        })

    return redirect("/")


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)
    games = cart.games.all()
    total = sum(game.price for game in games)

    return render(request, "store/cart.html", {
        "games": games,
        "total": total,
    })


def remove_from_cart(request, game_id):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(user=request.user)
    game = get_object_or_404(Game, id=game_id)

    cart.games.remove(game)

    return redirect("cart")


@login_required
def buy_all(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    library, created = Library.objects.get_or_create(user=request.user)

    for game in cart.games.all():
        LibraryGame.objects.get_or_create(
            library=library,
            game=game
        )

    cart.games.clear()

    return redirect("library")



def library_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    library, created = Library.objects.get_or_create(user=request.user)
    games = library.library_games.select_related("game")

    return render(request, "store/library.html", {"games": games})


@login_required
def library_detail(request, game_id):
    library = get_object_or_404(Library, user=request.user)
    game = get_object_or_404(Game, id=game_id)
    lib_game = get_object_or_404(LibraryGame, library=library, game=game)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in ["playing", "completed", "wishlist"]:
            lib_game.status = new_status
            lib_game.save()

        return redirect("library")

    return render(request, "store/library_detail.html", {
        "lib_game": lib_game,
        "game": game,
    })


def update_status(request, game_id):
    if request.method != "POST":
        return redirect("library")

    library = request.user.library
    library_game = get_object_or_404(LibraryGame, library=library, game_id=game_id)

    new_status = request.POST.get("status")
    if new_status in dict(LibraryGame.STATUS_CHOICES):
        library_game.status = new_status
        library_game.save()

    return redirect("library_detail", game_id=game_id)


def logout_view(request):
    logout(request)
    return redirect("login")
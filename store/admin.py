from django.contrib import admin
from .models import User, Game, Cart, Library, LibraryGame


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "dark_background", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("dark_background", "is_staff")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "price", "avg_rating")
    search_fields = ("title", "genre")
    list_filter = ("genre",)
    list_editable = ("price", "avg_rating")
    ordering = ("title",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price")
    search_fields = ("user__username", "user__email")


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


@admin.register(LibraryGame)
class LibraryGameAdmin(admin.ModelAdmin):
    list_display = ("library", "game", "status")
    list_filter = ("status",)
    search_fields = ("game__title", "library__user__username")

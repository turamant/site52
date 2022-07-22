from django.contrib import admin

from .models import Post, Category, Comment, Images


class CommentItemInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ('post',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'intro', 'created_at',
                    'status')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'intro', 'created_at')
    list_filter = ('category', 'created_at')
    inlines = (CommentItemInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'body', 'created_at')
    search_fields = ('name', 'post', 'email', 'body', 'created_at')
    list_filter = ('name', 'post', 'created_at')
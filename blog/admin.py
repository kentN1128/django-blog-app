from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from blog.models import Post, Category, Tag, Comment, Reply
# Register your models here.

class ReplyInline(admin.StackedInline):
    model =Reply

class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
class PostAdmin(MarkdownxModelAdmin,admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at', 'is_published')
    search_fields = ('title', 'content')
    list_filter = ('category',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply)

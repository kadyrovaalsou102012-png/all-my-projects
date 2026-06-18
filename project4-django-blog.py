# ==============================================================================
# ПРОЕКТНАЯ РАБОТА №4: Простой блог на фреймворке Django
# Задание: Регистрация, авторизация, создание, редактирование, просмотр и удаление статей,
# а также добавление комментариев в хронологическом порядке.
# ==============================================================================

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# ==================== 1. МОДЕЛИ ДАННЫХ (models.py) ====================
# Требование: Модель Article (заголовок, текст, дата создания, автор)
# Требование: Модель Comment (текст комментария, автор, связанная статья, дата)

class Article(models.Model):
    """Модель для публикаций (статей) блога"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        ordering = ['-created_at']  # Сначала новые статьи
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def str(self):
        return self.title


class Comment(models.Model):
    """Модель для комментариев под статьями"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="Статья")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        ordering = ['created_at']  # Комментарии отображаются в хронологическом порядке
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def str(self):
        return f"Комментарий от {self.author.username} к статье '{self.article.title}'"


# ==================== 2. НАСТРОЙКА АДМИН-ПАНЕЛИ (admin.py) ====================
# Требование: Регистрация моделей в admin.py для управления через панель администратора

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('created_at', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)


# ==================== 3. СХЕМА МАРШРУТОВ / URL (urls.py) ====================
# Требование: Настройка маршрутов (URLConf) для отображения страниц блога

urlpatterns = [
    path('', views.ArticleListView, name='blog_home'),
    path('article/<int:pk>/', views.ArticleDetailView, name='article_detail'),
    path('article/new/', views.ArticleCreateView, name='article_create'),
    path('article/<int:pk>/edit/', views.ArticleEditView, name='article_edit'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView, name='article_delete'),
]


# ==================== 4. ПРЕДСТАВЛЕНИЯ И ОБРАБОТКА ЗАПРОСОВ (views.py) ====================
# Требование: Просмотр списка статей, просмотр одной статьи, создание, редактирование и удаление.

def ArticleListView(request):
    """Отображение списка всех статей на главной странице"""
    articles = Article.objects.all()
    # Отображаем шаблон со списком переданных статей
    return render(request, 'blog/home.html', {'articles': articles})
  """Отображение одной конкретной статьи с комментариями к ней"""
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()  # Получаем все связанные комментарии
    
    # Обработка POST-запроса (chat request) на добавление комментария
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')  # Если не авторизован, отправляем на вход
            
        comment_text = request.POST.get('text')
        if comment_text:
            Comment.objects.create(
                article=article,
                author=request.user,
                text=comment_text
            )
            return redirect('article_detail', pk=article.pk)
            
    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments})


@login_required
def ArticleCreateView(request):
    """Создание новой статьи (только для авторизованных пользователей)"""
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:
            article = Article.objects.create(
                title=title,
                text=text,
                author=request.user
            )
            return redirect('article_detail', pk=article.pk)
            
    return render(request, 'blog/article_form.html')


@login_required
def ArticleEditView(request, pk):
    """Редактирование статьи (доступно только её автору)"""
    article = get_object_or_404(Article, pk=pk)
    
    # Ограничение доступа: редактировать может только создатель статьи
    if article.author != request.user:
        raise PermissionDenied
        
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:
            article.title = title
            article.text = text
            article.save()  # Сохраняем измененную статью в базу
            return redirect('article_detail', pk=article.pk)
            
    return render(request, 'blog/article_form.html', {'article': article})


@login_required
def ArticleDeleteView(request, pk):
    """Удаление статьи (chat delete — доступно только автору статьи)"""
    article = get_object_or_404(Article, pk=pk)
    
    # Ограничение доступа: удалить статью может только её автор
    if article.author != request.user:
        raise PermissionDenied
        
    if request.method == "POST":
        article.delete()  # Полное удаление объекта из базы данных
        return redirect('blog_home')  # Возврат на главную страницу после удаления
        
    return render(request, 'blog/article_confirm_delete.html', {'article': article})


def ArticleDetailView(request, pk):

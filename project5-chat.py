# ==============================================================================
# ОНЛАЙН-ЧАТ НА DJANGO (ЧАСТИ 1 И 2)
# Полный объединенный код: регистрация, комната чата, отправка, 
# редактирование, удаление сообщений и очистка истории чата.
# ==============================================================================

from django.db import models
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path

# ==================== 1. МОДЕЛИ ДАННЫХ (models.py) ====================

class User(models.Model):
    """Модель для хранения пользователей чата"""
    name = models.CharField(max_length=50, verbose_name="Имя пользователя")

    def str(self):
        return self.name


class Message(models.Model):
    """Модель для хранения сообщений чата"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст сообщения")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")

    def str(self):
        return f"{self.user.name}: {self.text[:20]}"


# ==================== 2. ФОРМЫ (forms.py) ====================

class UserForm(forms.Form):
    """Форма для регистрации/входа пользователя"""
    name = forms.CharField(label="Ваше имя", max_length=50)


class MessageForm(forms.Form):
    """Форма для отправки и редактирования сообщений в чате"""
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите текст...'}),
        max_length=500
    )


# ==================== 3. ПРЕДСТАВЛЕНИЯ И ОБРАБОТКА ЗАПРОСОВ (views.py) ====================

def register_user_view(request):
    """Представление для регистрации пользователя перед входом в чат"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create(name=form.cleaned_data['name'])
            request.session['chat_user_id'] = new_user.id
            return redirect('chat_room')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def chat_room_view(request):
    """Представление комнаты чата с выводом сообщений и формой отправки"""
    user_id = request.session.get('chat_user_id')
    if not user_id:
        return redirect('chat_register')

    current_user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                user=current_user,
                text=form.cleaned_data['message']
            )
            return redirect('chat_room')
    else:
        form = MessageForm()

    all_messages = Message.objects.all().order_by('timestamp')

    return render(request, 'chat.html', {
        'form': form,
        'current_user': current_user,
        'messages': all_messages
    })


def delete_message_view(request, message_id):
    """Удаление конкретного сообщения из чата (chat delete)"""
    user_id = request.session.get('chat_user_id')
    if not user_id:
        return redirect('chat_register')

    # Находим сообщение по id или выдаем 404 ошибку, если его нет
    message = get_object_or_404(Message, id=message_id)
    
    # Запрос на удаление объекта из базы данных
    message.delete()
    return redirect('chat_room')


def edit_message_view(request, message_id):
    """Редактирование существующего сообщения в чате (chat request/edit)"""
    user_id = request.session.get('chat_user_id')
    if not user_id:
        return redirect('chat_register')

    message = get_object_or_404(Message, id=message_id)
    current_user = User.objects.get(id=user_id)
  if form.is_valid():
            # Перезаписываем текст сообщения и сохраняем его
            message.text = form.cleaned_data['message']
            message.save()
            return redirect('chat_room')
    else:
        # Предзаполняем форму старым текстом сообщения
        form = MessageForm(initial={'message': message.text})

    return render(request, 'edit_message.html', {
        'form': form,
        'message': message,
        'current_user': current_user
    })


def clear_chat_view(request):
    """Полная очистка всей истории сообщений в чате"""
    user_id = request.session.get('chat_user_id')
    if not user_id:
        return redirect('chat_register')

    # Удаляем абсолютно все записи из таблицы Message
    Message.objects.all().delete()
    return redirect('chat_room')


# ==================== 4. МАРШРУТЫ И URL (urls.py) ====================

urlpatterns = [
    path('chat/register/', register_user_view, name='chat_register'),
    path('chat/', chat_room_view, name='chat_room'),
    path('chat/delete/<int:message_id>/', delete_message_view, name='delete_message'),
    path('chat/edit/<int:message_id>/', edit_message_view, name='edit_message'),
    path('chat/clear/', clear_chat_view, name='clear_chat'),
]

    if request.method == 'POST':
        form = MessageForm(request.POST)

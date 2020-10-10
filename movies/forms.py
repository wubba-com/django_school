from django import forms
from .models import Reviews


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')  # Здесь перечисляем поля из модели, которые нам ужны для работы с формами

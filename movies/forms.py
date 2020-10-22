from django import forms
from .models import Reviews, RatingStar, Rating
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""

    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = (
            'name', 'email', 'text', 'captcha'
        )  # Здесь перечисляем поля из модели, которые нам ужны для работы с формами
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'text': forms.Textarea()
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)

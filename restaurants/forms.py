from django import forms
from .models import Restaurant, FACILITY_OPTIONS


class RestaurantForm(forms.ModelForm):
    facilities = forms.MultipleChoiceField(
        choices=[(f, f) for f in FACILITY_OPTIONS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='편의시설',
    )

    rating_taste = forms.IntegerField(min_value=1, max_value=5, label='음식 맛 (1~5)')
    rating_mood = forms.IntegerField(min_value=1, max_value=5, label='분위기 (1~5)')
    rating_service = forms.IntegerField(min_value=1, max_value=5, label='서비스 (1~5)')

    class Meta:
        model = Restaurant
        fields = [
            'name', 'address', 'region', 'category', 'price_range', 'vibe',
            'facilities', 'meal_time', 'rating_taste', 'rating_mood', 'rating_service',
            'memo', 'photo', 'visited_date', 'revisit',
        ]
        widgets = {
            'visited_date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.facilities:
            self.initial['facilities'] = self.instance.facilities
        # photo는 선택사항
        self.fields['photo'].required = False

    def clean_facilities(self):
        return list(self.cleaned_data.get('facilities', []))

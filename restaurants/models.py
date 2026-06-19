from django.db import models
from django.conf import settings


REGION_CHOICES = [
    ('서울', '서울'), ('경기', '경기'), ('인천', '인천'), ('부산', '부산'),
    ('대구', '대구'), ('대전', '대전'), ('광주', '광주'), ('기타', '기타'),
]

CATEGORY_CHOICES = [
    ('한식', '한식'), ('일식', '일식'), ('중식', '중식'), ('양식', '양식'),
    ('카페', '카페'), ('디저트', '디저트'), ('술집', '술집'), ('기타', '기타'),
]

PRICE_CHOICES = [
    ('1만원이하', '1만원 이하'), ('1~3만원', '1~3만원'), ('3만원이상', '3만원 이상'),
]

VIBE_CHOICES = [
    ('조용한', '조용한'), ('활기찬', '활기찬'), ('로맨틱', '로맨틱'),
    ('캐주얼', '캐주얼'), ('비즈니스', '비즈니스'),
]

MEAL_TIME_CHOICES = [
    ('아침', '아침'), ('점심', '점심'), ('저녁', '저녁'),
]

FACILITY_OPTIONS = ['주차가능', '예약가능', '단체석', '포장가능']


class Restaurant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100, verbose_name='맛집 이름')
    address = models.CharField(max_length=200, verbose_name='주소')
    region = models.CharField(max_length=10, choices=REGION_CHOICES, verbose_name='지역')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name='음식종류')
    price_range = models.CharField(max_length=10, choices=PRICE_CHOICES, verbose_name='가격대')
    vibe = models.CharField(max_length=10, choices=VIBE_CHOICES, verbose_name='분위기')
    facilities = models.JSONField(default=list, blank=True, verbose_name='편의시설')
    meal_time = models.CharField(max_length=5, choices=MEAL_TIME_CHOICES, verbose_name='방문 시간대')
    rating_taste = models.IntegerField(verbose_name='음식 맛')
    rating_mood = models.IntegerField(verbose_name='분위기')
    rating_service = models.IntegerField(verbose_name='서비스')
    memo = models.TextField(blank=True, verbose_name='메모')
    photo = models.ImageField(upload_to='restaurants/', blank=True, null=True, verbose_name='사진')
    visited_date = models.DateField(null=True, blank=True, verbose_name='방문일')
    revisit = models.BooleanField(default=True, verbose_name='재방문 의향')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def rating_avg(self):
        return round((self.rating_taste + self.rating_mood + self.rating_service) / 3, 1)

import urllib.request
import os
import cloudinary
import cloudinary.uploader
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant

SEED_MAP = {
    "온지음 맛공간":           ("korean,food",      1),
    "광화문 국밥":             ("soup,korean",      2),
    "정식당":                  ("finedining,food",  3),
    "스시 사이토":             ("sushi,japanese",   4),
    "가온":                    ("korean,cuisine",   5),
    "연남동 경양식 1920":      ("restaurant,retro", 6),
    "망원동 오래된 국수":      ("noodle,soup",      7),
    "이태원 알레그리아":       ("tapas,wine",       8),
    "초량밀면":                ("noodle,cold",      9),
    "해운대 암소갈비집":       ("bbq,grill",        10),
    "범일동 할매국밥":         ("pork,soup",        11),
    "광안리 수변최고집":       ("seafood,ocean",    12),
    "제주 흑돼지 오겹살 본점": ("pork,grilled",     13),
    "성산 고등어쌈밥":         ("fish,grilled",     14),
    "카페 봄날 서귀포":        ("cafe,jeju",        15),
    "황리단길 쌈밥한상":       ("korean,table",     16),
    "인천 차이나타운 공화춘":  ("chinese,noodle",   17),
    "전주 한옥마을 가족회관":  ("bibimbap,korean",  18),
    "강릉 교동짬뽕":           ("spicy,noodle",     19),
    "테라로사 강릉 본점":      ("coffee,cafe",      20),
}


class Command(BaseCommand):
    help = "loremflickr 이미지를 Cloudinary에 업로드합니다."

    def handle(self, *args, **options):
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        )

        # 기존 사진 초기화
        Restaurant.objects.update(photo="")

        ok, fail, skip = 0, 0, 0

        for r in Restaurant.objects.all():

            entry = SEED_MAP.get(r.name)
            if not entry:
                self.stdout.write(f"  skip (not in map): {r.name}")
                skip += 1
                continue

            tags, lock = entry
            url = f"https://loremflickr.com/800/600/{tags}/all?lock={lock}"

            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    image_data = resp.read()

                result = cloudinary.uploader.upload(
                    image_data,
                    folder="mat_itda",
                    public_id=f"restaurant_{r.pk}",
                    overwrite=True,
                )
                r.photo = result['secure_url']
                r.save(update_fields=["photo"])
                self.stdout.write(self.style.SUCCESS(f"  OK [{lock}] {r.name}"))
                ok += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  FAIL: {r.name} -> {e}"))
                fail += 1

        self.stdout.write(self.style.SUCCESS(f"\nDone: OK={ok} / skip={skip} / fail={fail}"))

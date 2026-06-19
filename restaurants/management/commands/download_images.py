import urllib.request
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from restaurants.models import Restaurant

# loremflickr: /width/height/tag1,tag2/all?lock=N  → lock 번호별로 고정된 다른 사진
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
    help = "음식 이미지를 재다운로드해서 DB에 연결합니다."

    def handle(self, *args, **options):
        media_dir = Path(settings.MEDIA_ROOT) / "restaurants"
        media_dir.mkdir(parents=True, exist_ok=True)

        # 기존 이미지 초기화
        Restaurant.objects.update(photo="")

        ok, fail = 0, 0

        for r in Restaurant.objects.all():
            entry = SEED_MAP.get(r.name)
            if not entry:
                self.stdout.write(f"  skip: {r.pk}")
                continue

            tags, lock = entry
            filename = f"{r.pk}_{lock}.jpg"
            filepath = media_dir / filename
            url = f"https://loremflickr.com/800/600/{tags}/all?lock={lock}"

            # 기존 파일 제거
            if filepath.exists():
                filepath.unlink()

            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    filepath.write_bytes(resp.read())

                r.photo = f"restaurants/{filename}"
                r.save(update_fields=["photo"])
                self.stdout.write(self.style.SUCCESS(f"  OK [{lock}] {r.name}"))
                ok += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  FAIL: {r.name} -> {e}"))
                fail += 1

        self.stdout.write(self.style.SUCCESS(f"\nDone: OK={ok} / fail={fail}"))

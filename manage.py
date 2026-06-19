#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 임포트할 수 없습니다. 가상환경이 활성화되어 있고 "
            "requirements.txt가 설치되어 있는지 확인하세요."
        ) from exc
    execute_from_command_line(sys.argv)

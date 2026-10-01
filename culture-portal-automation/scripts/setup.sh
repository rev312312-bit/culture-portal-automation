#!/usr/bin/env bash
# Codespaces(또는 리눅스/맥 터미널)에서 한 번 실행하는 설치 스크립트
set -e
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m playwright install --with-deps chromium
[ -f .env ] || cp .env.example .env
echo ""
echo "설치 완료!"
echo "1) .env 파일을 열어 SERVICE_KEY 값을 넣으세요."
echo "2) python3 scripts/check_connection.py 로 접속을 확인하세요."

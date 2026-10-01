#!/usr/bin/env bash
# Codespaces(또는 리눅스/맥 터미널)에서 한 번 실행하는 설치 스크립트
set -e
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
# Codespaces 기본 이미지의 만료된 yarn 저장소 설정이 브라우저 설치를 막는 문제 회피
sudo rm -f /etc/apt/sources.list.d/yarn* 2>/dev/null || true
# Git LFS 미설치 경고 제거 (이 프로젝트는 LFS 를 쓰지 않음)
rm -f .git/hooks/pre-push .git/hooks/post-merge .git/hooks/post-checkout .git/hooks/post-commit
python3 -m playwright install --with-deps chromium
echo ""
echo "설치 완료!"
echo "1) .env 파일을 열어 SERVICE_KEY 값을 넣으세요."
echo "2) python3 scripts/check_connection.py 로 접속을 확인하세요."

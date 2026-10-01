# 출처: 팀 TC FN_INFO_001~010 (즐겨요 문화정보 > 한눈에 보는 문화정보)
# 태그 규칙
#   @tc_<팀 TC ID>          수동 TC와의 추적성
#   @defect_<결함 ID>       이미 보고된 결함 — 결함이 남아 있으면 '예상된 실패(xfail)'로 처리됨
#   @smoke / @regression    실행 범위
Feature: 한눈에 보는 문화정보 검색
  문화정보를 검색하는 사용자는 잘못된 검색어를 입력했을 때 안내를 받고,
  올바른 검색어로는 결과를 볼 수 있어야 한다.

  Background:
    Given 한눈에 보는 문화정보 화면에 접속함

  @tc_FN_INFO_001 @defect_INFO_DF_001 @regression
  Scenario: UI-검색-필수값-001 검색어 없이 검색
    When 검색어 "" 로 검색함
    Then "최소 두자리 이상의 검색어를 입력하세요" 안내 메시지가 노출됨

  @tc_FN_INFO_002 @defect_INFO_DF_002 @regression
  Scenario: UI-검색-필수값-002 공백 2칸만 입력하고 검색
    When 검색어 "  " 로 검색함
    Then "최소 두자리 이상의 검색어를 입력하세요" 안내 메시지가 노출됨

  @tc_FN_INFO_003 @defect_INFO_DF_003 @regression
  Scenario: UI-검색-경계값-001 앞 공백과 한 글자로 검색
    When 검색어 " 문" 로 검색함
    Then "최소 두자리 이상의 검색어를 입력하세요" 안내 메시지가 노출됨

  @tc_FN_INFO_004 @smoke
  Scenario: UI-검색-정상-001 앞뒤 공백이 있는 검색어로 검색
    When 검색어 " 축제 " 로 검색함
    Then 안내 메시지 없이 검색 결과가 1건 이상 노출됨

  @tc_FN_INFO_005 @smoke
  Scenario: UI-상세검색-토글-001 상세검색 열기와 닫기
    When 상세검색 버튼을 클릭함
    Then 상세검색 버튼 문구가 바뀜
    When 상세검색 버튼을 클릭함
    Then 상세검색 버튼 문구가 처음과 같아짐

  @tc_FN_INFO_010 @regression
  Scenario: UI-상세검색-초기화-001 전체해제로 필터 초기화
    Given 상세검색을 열고 필터를 3개 선택함
    When 전체해제 버튼을 클릭함
    Then 선택된 필터가 0개임

# 출처: 팀 TC FN_INFO_027~028 (즐겨요 문화정보 > 문화캘린더)
Feature: 문화캘린더 월 표시와 이동
  사용자는 캘린더에서 이번 달을 기본으로 보고, 이전 달과 다음 달로 이동할 수 있어야 한다.

  Background:
    Given 문화캘린더 화면에 접속함

  @tc_FN_INFO_027 @smoke
  Scenario: UI-캘린더-표시-001 이번 달 기본 표시
    Then 캘린더 제목에 오늘의 연월이 표시됨

  # 팀 리뷰에서 '이전/다음 두 동작이 한 TC에 있어 추적 불가'로 지적되어 분리함
  @tc_FN_INFO_028 @regression
  Scenario: UI-캘린더-이동-001 이전 달로 이동
    When 이전 달 버튼을 클릭함
    Then 캘린더 제목이 한 달 전 연월로 바뀜

  @tc_FN_INFO_028 @regression
  Scenario: UI-캘린더-이동-002 다음 달로 이동
    When 다음 달 버튼을 클릭함
    Then 캘린더 제목이 한 달 뒤 연월로 바뀜

# CLAUDE.md

> **반드시 따를 것**: `../clae/CLAUDE.md` 읽고 9단계 플로우 따라갈 것
>
> **clae 로컬 경로**: `../clae/` (같은 work 디렉토리 내 형제 폴더)
>
> **clae 경로 못 찾으면**: 사용자에게 경로 질문 (GitHub: https://github.com/jongsup-baek/clae)
>
> **세션 종료 전 필수**: 3절 작업 이력에 오늘 작업 요약 기록 (다음 세션에서 이어서 작업 가능하도록)

**관련 GitHub repo:**

- [jongsup-baek/clae](https://github.com/jongsup-baek/clae) — CLAE 협업 지식 베이스, 프로젝트 전체 이슈 관리
- [jongsup-baek/claeclassmaster](https://github.com/jongsup-baek/claeclassmaster) — 교재 개발 원칙 + 액티브 리뷰 (상위 레포)
- [jongsup-baek/claeclassmaster_quizbank](https://github.com/jongsup-baek/claeclassmaster_quizbank) — 이 프로젝트 - 퀴즈 문제 은행
- [jongsup-baek/class_svbasic](https://github.com/jongsup-baek/class_svbasic) — 반도체설계검증언어기초 (퀴즈 소비 레포)

> **내 역할**: 퀴즈 관리 — class_ 교재를 읽고 문제 작성, YAML 등록, 난이도 관리. class_ 파일은 읽기만.
> **병렬 워크플로우**: `../claeclassmaster/principles/workflow_roles.md` 참조

---

## 1. 프로젝트 개요

YAML 기반 퀴즈 문제 은행. 전체 교육 과정의 퀴즈를 중앙 관리한다.

- 문제 저장: `questions/` (과목별 YAML)
- 퀴즈 작성 원칙: `principles/` (이 레포에서 관리)
- 슬라이드 포맷 원칙: `principles/quiz_rules.md` (이 레포에서 관리, clae #35)
- 검증 도구: `../claeclassmaster/tools/quiz_validator.py` 참조

## 2. 작업 원칙

### 2.1 문제 YAML 형식

```yaml
- id: {과목}_{강의번호}_{순번}     # 예: svbasic_02_001
  section: "X.Y"                    # 강의번호.섹션번호
  section_title: "섹션 제목"
  question: "질문 텍스트"
  choices:
    - "선택지 1"
    - "선택지 2"
    - "선택지 3"
    - "선택지 4"
  answer: N                         # 정답 번호 (1-based)
  difficulty: 하|중|상              # principles/quiz_rules.md 난이도 기준 참조
  has_code: false                   # 코드 블록 포함 여부
  code: |                           # has_code: true일 때만
    코드 내용
  explanation:
    - "해설 포인트 1"
    - "해설 포인트 2"
    - "해설 포인트 3"
  created: YYYY-MM-DD
```

### 2.2 파일 네이밍

- `questions/{과목}/class{NN}_{영문주제}.yaml`
- 예: `questions/svbasic/class02_data_types.yaml`

### 2.3 난이도 판별

`principles/quiz_rules.md`의 난이도 기준 및 판별 체크리스트를 따른다.

### 2.4 워크플로우

1. 강의 내용 기반으로 문제 작성 → YAML로 이 레포에 등록
2. claeclassmaster가 원칙 기반 검증
3. YAML → Marp 슬라이드 변환 → class_ 레포 lecture_{과목명}/에 배포

## 3. 작업 이력

> **Git Issue로 관리**: 세션 종료 전 `gh issue create --label history`로 작업 이력 발급

---

*Authored-By: Jongsup Baek <jongsup.baek@ksdcsemi.com>*
*Last updated: 2026-03-02*

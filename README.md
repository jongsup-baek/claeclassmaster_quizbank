# claeclassmaster_quizbank

> YAML 기반 퀴즈 문제 은행 — 전 교육 과정 퀴즈 중앙 관리

---

## 1. 소개

교육 자료의 퀴즈를 중앙에서 관리하는 문제 은행.
강의 내용 기반으로 문제를 YAML로 작성하고, Marp 슬라이드로 변환하여 각 class_ 레포에 배포한다.

- 문제 작성: class_ 교재를 읽고 YAML로 등록
- 난이도 관리: claeclassmaster `principles/quiz_rules.md` 기준
- 변환 도구: YAML → Marp 슬라이드 자동 생성
- 배포: class_ 레포 `lecture_{과목명}/`에 퀴즈 Marp 배치

## 2. 구조

- 문제 YAML (과목별 퀴즈 데이터) — `questions/`
- 변환 도구 (YAML → Marp 변환) — `tools/` (개발 예정)

### questions/ 구조

```
questions/
├── svbasic/
│   ├── class02_data_types.yaml
│   ├── class03_procedural.yaml    (예정)
│   └── ...
├── ipverif/                       (예정)
└── ...
```

## 3. 관련 레포

| 레포 | 관계 |
|------|------|
| claeclassmaster | 상위 레포 — 퀴즈 작성 원칙, 검증 도구 |
| class_svbasic | 퀴즈 소비 레포 — lecture_svbasic/에 Marp 배포 |
| clae | CLAE 협업 지식 베이스 |

---

*Authored-By: Jongsup Baek <jongsup.baek@ksdcsemi.com>*
*Last updated: 2026-03-02*

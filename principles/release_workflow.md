# 릴리즈 워크플로우

> 퀴즈뱅크에서 릴리즈/배포 요청 시 따를 절차

---

## 1. 용어 정의

| 용어 | 의미 | 도구 |
|------|------|------|
| **릴리즈** | lecture marp → PPTX/PDF 빌드 | `build_deck.py --both` |
| **lab 업데이트** | lab 코드 → GitHub class org template/학생 레포 push | git push |

## 2. 릴리즈 (강의 슬라이드)

"릴리즈"는 항상 **class 레벨** (lecture marp 기준)이다.

### 절차

1. 퀴즈 배포: `deploy_quiz.py -s {과목}`
2. 릴리즈 빌드: `build_deck.py --both --chunk 1 .../marp/classNN_topic_marp.md`
3. 출력: `{semester}/release/classNN_topic_deck.{pptx,pdf}`

### 퀴즈 없는 강의

퀴즈가 없는 class는 `--chunk 1` 없이 빌드:
```
build_deck.py --both .../marp/classNN_topic_marp.md
```

## 3. Lab 업데이트

**lab 관리 및 GitHub Classroom 배포는 course_ 세션의 역할이다** (`workflow_roles.md` 참조).
quizbank 세션에서는 lab을 다루지 않는다.

- lab 관리: course_sv / course_uvm / course_semiconintro 세션
- GitHub Classroom org: `ksdcsemi-class`
  - template 레포: `svbasic-template` (is_template=true)
  - 학생 레포: `svbasic-kyu-2026-1-{학생ID}` (template에서 생성됨)

---

*Authored-By: Jongsup Baek <jongsup.baek@ksdcsemi.com>*
*Last updated: 2026-03-04*

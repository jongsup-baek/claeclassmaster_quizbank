# 이미지 활용 원칙

> 퀴즈 문제에서 교재 이미지를 활용하기 위한 원칙

---

## 1. 기본 방침

- 교재에서 이미 사용된 이미지(다이어그램, 코드 예제 그림)를 퀴즈에 활용한다.
- 새로운 이미지를 별도로 제작하지 않는다.
- 이미지는 학습 효과를 높이기 위한 보조 자료로 활용한다.

## 2. YAML 필드

```yaml
has_image: true                              # 이미지 포함 여부
image: "./images/classNN_X_Y.drawio.svg"     # 교재 원본 경로
image_alt: "이미지 설명"                     # 대체 텍스트
```

- `has_image: false`이면 `image`, `image_alt` 필드는 생략 가능
- `image` 경로는 교재 원본(class_ 레포) 기준 상대 경로
- YAML → Marp 변환 스크립트가 경로를 자동 변환

## 3. 적용 기준

- 각 섹션의 첫 번째 문제에 해당 섹션 이미지를 연결한다.
- 두 번째 문제는 개념 확인 문제로 이미지 없이 출제한다.
- 이미지가 문제 풀이에 직접 필요한 경우, 질문 텍스트에 "다음 그림을 참고하여" 등의 안내를 포함한다.

## 4. 경로 규칙

- 교재 이미지 경로: `./images/class{NN}_{X}_{Y}.drawio.svg`
  - `NN`: 강의 번호 (예: 03)
  - `X_Y`: 섹션 번호 (예: 3_2)
- 변환 스크립트에서 quizbank 경로 → class_ 레포 경로로 자동 변환

---

*Authored-By: Jongsup Baek <jongsup.baek@ksdcsemi.com>*
*Last updated: 2026-03-02*

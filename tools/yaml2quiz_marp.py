#!/usr/bin/env python3
"""YAML 퀴즈 → Marp 슬라이드 변환 스크립트.

Usage:
    python yaml2quiz_marp.py <yaml_file> [--output <output_file>] [--image-base <path>]

Examples:
    python yaml2quiz_marp.py questions/svbasic/class03_procedural.yaml
    python yaml2quiz_marp.py questions/svbasic/class03_procedural.yaml --output out.md
    python yaml2quiz_marp.py questions/svbasic/class03_procedural.yaml --image-base ../images
"""

import argparse
import sys
from collections import OrderedDict
from pathlib import Path

import yaml


# --- 과목 메타데이터 ---
COURSE_META = {
    "svbasic": {
        "course_name": "반도체설계검증언어기초",
        "university": "건양대학교 국방반도체공학과",
        "professor": "백종섭 교수",
    },
    "semiconintro_dyc": {
        "course_name": "반도체개론",
        "university": "건양대학교 국방반도체공학과",
        "professor": "백종섭 교수",
    },
}

# --- 강의 제목 매핑 ---
LECTURE_TITLES = {
    "svbasic": {
        "02": "기본 데이터 타입과 리터럴",
        "03": "절차문과 절차 블록",
    },
}


def load_yaml(yaml_path: Path) -> list[dict]:
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_file_info(yaml_path: Path) -> dict:
    """파일명에서 과목, 강의번호, 영문주제 추출."""
    stem = yaml_path.stem  # e.g. "class03_procedural"
    parts = stem.split("_", 1)
    class_num = parts[0].replace("class", "")  # "03"
    topic_eng = parts[1] if len(parts) > 1 else ""  # "procedural"

    subject = yaml_path.parent.name  # e.g. "svbasic"
    return {
        "subject": subject,
        "class_num": class_num,
        "topic_eng": topic_eng,
    }


def get_lecture_title(subject: str, class_num: str) -> str:
    return LECTURE_TITLES.get(subject, {}).get(class_num, "")


def group_by_section(questions: list[dict]) -> OrderedDict:
    """섹션별로 문제를 그룹화."""
    groups = OrderedDict()
    for q in questions:
        sec = q["section"]
        if sec not in groups:
            groups[sec] = []
        groups[sec].append(q)
    return groups


def render_choices(choices: list[str]) -> str:
    lines = []
    for i, choice in enumerate(choices, 1):
        lines.append(f"&emsp;{i}\\) {choice}")
    return "\n".join(lines)


def render_code_block(q: dict) -> str:
    if not q.get("has_code", False) or not q.get("code"):
        return ""
    code = q["code"].rstrip("\n")
    return f"\n```systemverilog\n{code}\n```\n"


def render_image(q: dict, image_base: str | None) -> str:
    if not q.get("has_image", False) or not q.get("image"):
        return ""
    image_path = q["image"]
    if image_base:
        filename = Path(image_path).name
        image_path = f"{image_base}/{filename}"
    alt = q.get("image_alt", "")
    return f"![w:400 {alt}]({image_path})"


def render_question_page(q: dict, q_num: int, section_idx: int,
                         section_total: int, image_base: str | None) -> str:
    sec = q["section"]
    title = q["section_title"]
    code_block = render_code_block(q)
    image_block = render_image(q, image_base)
    has_right_panel = bool(image_block or code_block)

    has_image = bool(image_block)
    has_right = has_image or bool(code_block)

    lines = [
        "<!-- _class: quiz -->",
        "",
        f"## Quiz 🔖 {sec} {title} ({section_idx}/{section_total}) (문제)",
    ]

    # 2단 레이아웃: 이미지 또는 코드가 있으면 columns 시작
    if has_right:
        lines.extend(["", '<div class="columns"><div>', ""])

    lines.extend([
        "",
        f"📌 문제 {q_num}. {q['question']}",
        "",
        render_choices(q["choices"]),
        "",
        "✍️ 문제를 풀어보세요",
    ])

    if has_right:
        right_content = image_block if has_image else code_block
        lines.extend([
            "",
            '</div><div>',
            "",
            right_content,
            "",
            '</div></div>',
        ])

    return "\n".join(lines)


def render_answer_page(q: dict, q_num: int, section_idx: int,
                       section_total: int, image_base: str | None) -> str:
    sec = q["section"]
    title = q["section_title"]
    code_block = render_code_block(q)
    image_block = render_image(q, image_base)
    has_image = bool(image_block)
    has_right = has_image or bool(code_block)

    lines = [
        "<!-- _class: quiz -->",
        "",
        f"## Quiz 🔖 {sec} {title} ({section_idx}/{section_total}) (해답)",
    ]

    if has_right:
        lines.extend(["", '<div class="columns"><div>', ""])

    lines.extend([
        "",
        f"📌 문제 {q_num}. {q['question']}",
        "",
        render_choices(q["choices"]),
        "",
        f"✅ 정답: {q['answer']}",
        f"⭐ 난이도: {q['difficulty']}",
        "",
        "💡 해설:",
    ])

    for exp in q.get("explanation", []):
        lines.append(f"- {exp}")

    if has_right:
        right_content = image_block if has_image else code_block
        lines.extend([
            "",
            '</div><div>',
            "",
            right_content,
            "",
            '</div></div>',
        ])

    return "\n".join(lines)


def render_frontmatter(subject: str, class_num: str) -> str:
    meta = COURSE_META.get(subject, COURSE_META["svbasic"])
    lecture_title = get_lecture_title(subject, class_num)
    header_text = f"{class_num}강 Quiz - {lecture_title}" if lecture_title else f"{class_num}강 Quiz"

    lines = [
        "---",
        "marp: true",
        "theme: konyang",
        "paginate: true",
        f'header: "{header_text}"',
        f'footer: "Copyright 2025. 한국반도체설계(주) KSDC Semi, Jongsup Baek. All rights reserved"',
        "---",
    ]
    return "\n".join(lines)


def render_title_page(subject: str, class_num: str) -> str:
    meta = COURSE_META.get(subject, COURSE_META["svbasic"])
    lecture_title = get_lecture_title(subject, class_num)
    subtitle = f"{class_num}강 Quiz: {lecture_title}" if lecture_title else f"{class_num}강 Quiz"

    lines = [
        "<!-- _class: title -->",
        '<!-- _header: "" -->',
        '<!-- _footer: "" -->',
        "<!-- _paginate: false -->",
        "",
        f"# {meta['course_name']}",
        "",
        subtitle,
        "",
        "<br><br><br><br><br><br>",
        f"{meta['university']}<br>{meta['professor']}",
    ]
    return "\n".join(lines)


def convert(yaml_path: Path, image_base: str | None = None) -> str:
    questions = load_yaml(yaml_path)
    info = parse_file_info(yaml_path)
    sections = group_by_section(questions)

    # 프론트매터 (--- 로 닫히므로 별도 처리)
    frontmatter = render_frontmatter(info["subject"], info["class_num"])

    # 슬라이드 페이지들
    slides = []

    # 타이틀 페이지
    slides.append(render_title_page(info["subject"], info["class_num"]))

    # 문제/해답 페이지
    q_num = 0
    for sec, sec_questions in sections.items():
        section_total = len(sec_questions)
        for section_idx, q in enumerate(sec_questions, 1):
            q_num += 1
            slides.append(render_question_page(
                q, q_num, section_idx, section_total, image_base))
            slides.append(render_answer_page(
                q, q_num, section_idx, section_total, image_base))

    # Thank You 페이지
    slides.append("## Thank You")

    return frontmatter + "\n\n" + "\n\n---\n\n".join(slides) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="YAML 퀴즈 → Marp 슬라이드 변환")
    parser.add_argument("yaml_file", help="입력 YAML 파일 경로")
    parser.add_argument("--output", "-o", help="출력 파일 경로 (미지정 시 stdout)")
    parser.add_argument("--image-base",
                        help="이미지 경로 베이스 (변환 시 이미지 경로 치환)")
    args = parser.parse_args()

    yaml_path = Path(args.yaml_file)
    if not yaml_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {yaml_path}", file=sys.stderr)
        sys.exit(1)

    result = convert(yaml_path, args.image_base)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"변환 완료: {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()

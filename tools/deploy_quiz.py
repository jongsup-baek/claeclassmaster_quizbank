#!/usr/bin/env python3
"""퀴즈 YAML → Marp 변환 + class 레포 배포 스크립트.

Usage:
    python tools/deploy_quiz.py --all
    python tools/deploy_quiz.py --subject svbasic
    python tools/deploy_quiz.py questions/svbasic/class03_procedural.yaml
"""

import argparse
import shutil
import sys
from pathlib import Path

import yaml

# 이 스크립트와 같은 디렉토리의 yaml2quiz_marp 모듈 임포트
sys.path.insert(0, str(Path(__file__).parent))
from yaml2quiz_marp import auto_output_name, convert


def load_deploy_config(repo_root: Path) -> dict:
    config_path = repo_root / "deploy.yaml"
    if not config_path.exists():
        print(f"오류: {config_path} 를 찾을 수 없습니다", file=sys.stderr)
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(repo_root: Path, rel: str) -> Path:
    return (repo_root / rel).resolve()


def deploy_single(yaml_path: Path, config: dict, repo_root: Path) -> str:
    """단일 YAML 파일 변환 + 배포. 배포된 파일 경로를 반환."""
    subject = yaml_path.parent.name
    if subject not in config:
        print(f"  건너뜀: {subject}이(가) deploy.yaml에 없음", file=sys.stderr)
        return ""

    cfg = config[subject]
    image_base = cfg.get("image_base")
    deploy_dir = resolve_path(repo_root, cfg["deploy_to"])

    result = convert(yaml_path, image_base)
    out_name = auto_output_name(yaml_path)
    out_path = deploy_dir / out_name

    deploy_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    return str(out_path)


def sync_theme(config: dict, repo_root: Path, subjects: list[str]) -> list[str]:
    """테마 CSS 동기화. 복사된 파일 목록 반환."""
    copied = []
    for subject in subjects:
        if subject not in config:
            continue
        cfg = config[subject]
        src = resolve_path(repo_root, cfg.get("theme_src", ""))
        dst = resolve_path(repo_root, cfg.get("theme_dst", ""))
        if src.exists() and src != dst:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(str(dst))
    return copied


def main():
    parser = argparse.ArgumentParser(
        description="퀴즈 YAML → Marp 변환 + class 레포 배포")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true",
                       help="모든 과목의 전체 YAML 변환 + 배포")
    group.add_argument("--subject", "-s",
                       help="특정 과목만 배포 (예: svbasic)")
    group.add_argument("yaml_file", nargs="?",
                       help="단일 YAML 파일 변환 + 배포")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    config = load_deploy_config(repo_root)

    deployed = []
    themes = []

    if args.yaml_file:
        yaml_path = Path(args.yaml_file).resolve()
        if not yaml_path.exists():
            print(f"오류: {yaml_path} 를 찾을 수 없습니다", file=sys.stderr)
            sys.exit(1)
        out = deploy_single(yaml_path, config, repo_root)
        if out:
            deployed.append(out)
        subject = yaml_path.parent.name
        themes = sync_theme(config, repo_root, [subject])

    else:
        subjects = [args.subject] if args.subject else list(config.keys())
        for subject in subjects:
            if subject not in config:
                print(f"오류: {subject}이(가) deploy.yaml에 없음",
                      file=sys.stderr)
                sys.exit(1)
            q_dir = resolve_path(repo_root, config[subject]["questions_dir"])
            yaml_files = sorted(q_dir.glob("class*.yaml"))
            if not yaml_files:
                print(f"  {subject}: YAML 파일 없음", file=sys.stderr)
                continue
            for yf in yaml_files:
                out = deploy_single(yf, config, repo_root)
                if out:
                    deployed.append(out)
        themes = sync_theme(config, repo_root, subjects)

    # 결과 리포트
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"배포 완료: {len(deployed)}개 파일", file=sys.stderr)
    for d in deployed:
        print(f"  ✅ {d}", file=sys.stderr)
    if themes:
        print(f"테마 동기화: {len(themes)}개", file=sys.stderr)
        for t in themes:
            print(f"  🎨 {t}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)


if __name__ == "__main__":
    main()

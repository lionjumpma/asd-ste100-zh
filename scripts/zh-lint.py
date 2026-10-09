#!/usr/bin/env python3
"""提示中文技术文本中的候选歧义；不判定语义或标准合规。"""

import argparse
import json
import re
import sys
from pathlib import Path

RULES = (
    ("vague-condition", re.compile(r"必要时|视情况|酌情|适当|及时|尽快"),
     "检查是否给出了可执行的触发条件或时间标准。"),
    ("unclear-reference", re.compile(r"它|该项|上述|相关(?:内容|结果|文件|操作)"),
     "检查指代是否只有一个明确对象。"),
    ("empty-praise", re.compile(r"无缝|强大|高效|一站式|智能化"),
     "删除无依据的评价，或改用可核查的事实。"),
    ("nominalized-action", re.compile(
        r"进行.{0,8}(?:处理|校验|分析|检查)|执行.{0,8}(?:操作|处理)"),
     "检查能否直接写出执行者和动作。"),
    ("stacked-hedge", re.compile(
        r"(?:可能|也许|或许|大概|预计).{0,12}(?:可能|也许|或许|大概|预计)"),
     "检查多个不确定词是否各有独立含义。"),
)

BACKTICK = chr(96)
INLINE_CODE = re.compile(re.escape(BACKTICK) + r"[^" + BACKTICK + r"]*" + re.escape(BACKTICK))
URL = re.compile(r"https?://[^\s)）]+")


def lint(text, filename="<stdin>"):
    findings = []
    in_fence = False
    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith((BACKTICK * 3, "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # 用等长空格保留原文中的列位置。
        visible = INLINE_CODE.sub(lambda m: " " * len(m.group()), line)
        visible = URL.sub(lambda m: " " * len(m.group()), visible)
        for rule, pattern, message in RULES:
            for match in pattern.finditer(visible):
                findings.append({
                    "file": filename,
                    "line": line_no,
                    "column": match.start() + 1,
                    "rule": rule,
                    "text": match.group(),
                    "message": message,
                })
    return sorted(findings, key=lambda x: (x["line"], x["column"], x["rule"]))


def selftest():
    rules = {item["rule"] for item in lint("必要时删除它。")}
    assert {"vague-condition", "unclear-reference"} <= rules
    assert lint(BACKTICK * 3 + "\n必要时删除它。\n" + BACKTICK * 3) == []
    assert lint("运行 " + BACKTICK + "必要时删除它" + BACKTICK + "。") == []
    assert lint("https://example.com/及时") == []
    print("selftest OK")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="UTF-8 文本文件；未指定时读取标准输入")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--fail-on-findings", action="store_true",
                        help="发现候选问题时返回退出码 1")
    parser.add_argument("--selftest", action="store_true", help="运行内置自检")
    args = parser.parse_args(argv)

    if args.selftest:
        selftest()
        return 0

    findings = []
    if args.files:
        for filename in args.files:
            findings.extend(lint(Path(filename).read_text(encoding="utf-8"), filename))
    else:
        findings.extend(lint(sys.stdin.read()))

    if args.json:
        print(json.dumps({"count": len(findings), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f'{item["file"]}:{item["line"]}:{item["column"]} '
                  f'{item["rule"]}: {item["text"]} — {item["message"]}')
        print(f"{len(findings)} 处候选问题；需人工判断，不能作为合规结论。")
    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())

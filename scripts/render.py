"""根据 data/projects.json 生成文档里的项目表格，可选刷新星数。

用法：
  python scripts/render.py            # 只按 projects.json 重新生成表格
  python scripts/render.py --refresh  # 先从 GitHub API 刷新星数和更新时间（建议设置 GITHUB_TOKEN）

表格写在目标文件的 <!-- BEGIN:projects --> 和 <!-- END:projects --> 之间。
只用 Python 标准库。MIT License.
"""
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "projects.json")


def fetch(repo, token):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "awesome-deepseek-harness-zh",
                 **({"Authorization": f"Bearer {token}"} if token else {})},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    return d["stargazers_count"], d["pushed_at"][:10], d.get("archived", False)


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def table(section):
    rows = [f"### {section['section']}", "", "| 项目 | 说明 | ⭐ | 最近更新 |", "|---|---|--:|---|"]
    for it in sorted(section["items"], key=lambda x: -x["stars"]):
        flag = "（已归档）" if it.get("archived") else ""
        rows.append(f"| [{it['repo']}](https://github.com/{it['repo']}) | {it['desc']}{flag} | {fmt(it['stars'])} | {it['pushed']} |")
    return "\n".join(rows)


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    if "--refresh" in sys.argv:
        token = os.environ.get("GITHUB_TOKEN", "")
        for sec in data["sections"]:
            for it in sec["items"]:
                try:
                    it["stars"], it["pushed"], it["archived"] = fetch(it["repo"], token)
                except urllib.error.HTTPError as e:
                    print(f"跳过 {it['repo']}：HTTP {e.code}")
        data["updated"] = datetime.date.today().isoformat()
        json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(DATA, "a", encoding="utf-8").write("\n")

    by_file = {}
    for sec in data["sections"]:
        by_file.setdefault(sec["file"], []).append(table(sec))
    for rel, blocks in by_file.items():
        path = os.path.join(ROOT, rel)
        text = open(path, encoding="utf-8").read()
        body = f"> 星数和更新时间截至 {data['updated']}，每周自动刷新。\n\n" + "\n\n".join(blocks)
        new, n = re.subn(r"(<!-- BEGIN:projects -->\r?\n).*?(<!-- END:projects -->)",
                         lambda m: m.group(1) + body + "\n" + m.group(2), text, flags=re.S)
        if n != 1:
            sys.exit(f"{rel} 里没有找到唯一的 BEGIN/END:projects 标记")
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        print(f"已更新 {rel}（{len(blocks)} 个分类）")


if __name__ == "__main__":
    main()

"""
Seed / fallback content.

This is the real data already sitting in the original README (dates, repos,
descriptions, star/fork counts) — reused so the rebuilt gallery renders with
genuine-looking content immediately instead of "lorem ipsum" placeholders.

"flag" / "cat" are Twemoji icon *names* (assets/emoji-src/<name>.png), not
raw unicode — this matches exactly what fetch_trending.py now writes into
data/repo_of_day.json and data/trending.json, so generate_cards.py treats
seed data and live data identically. See tokens.py's COUNTRY_FLAG_ICON /
REPO_CATEGORY_ICON for the keyword tables that produced these values.

fetch_trending.py overwrites data/repo_of_day.json and data/trending.json
with fresh picks on each run. If a fetch ever fails, the workflow falls back
to whatever those JSON files already contain (yesterday's picks) rather than
falling back to this file — this module is only used to *seed* the JSON
files the first time the pipeline runs, or ad-hoc for local preview.
"""

LANGUAGE_COLORS = {
    "JavaScript": ("#F7DF1E", "#1B1F27"),
    "TypeScript": ("#3178C6", "#FFFFFF"),
    "Python": ("#3776AB", "#FFFFFF"),
    "Go": ("#00ADD8", "#FFFFFF"),
    "HTML": ("#E34F26", "#FFFFFF"),
    "Swift": ("#F05138", "#FFFFFF"),
    "Perl": ("#39457E", "#FFFFFF"),
    "C++": ("#00599C", "#FFFFFF"),
    "Rust": ("#DE7A22", "#FFFFFF"),
    None: ("#6E7681", "#FFFFFF"),
}

REPO_OF_DAY = [
    {"date": "Jul 8", "flag": "flag-intl", "cat": "robot", "repo": "DietrichGebert/ponytail", "desc": "Makes your AI agent think like the laziest senior dev in the room — the best code is the code you don't write.", "lang": "JavaScript", "stars": "77k", "forks": "4.1k"},
    {"date": "Jul 7", "flag": "flag-cn", "cat": "robot", "repo": "baidu/Unlimited-OCR", "desc": "Unlimited OCR Works: welcome the era of one-shot long-horizon parsing.", "lang": "Python", "stars": "14k", "forks": "1.1k"},
    {"date": "Jul 6", "flag": "flag-intl", "cat": "brain", "repo": "XiaomiMiMo/MiMo-Code", "desc": "MiMo Code: where models and agents co-evolve.", "lang": "TypeScript", "stars": "12k", "forks": "1.1k"},
    {"date": "Jul 5", "flag": "flag-us", "cat": "robot", "repo": "langchain-ai/openwiki", "desc": "A CLI that writes and maintains agent documentation for your codebase.", "lang": "TypeScript", "stars": "9.5k", "forks": "617"},
    {"date": "Jul 4", "flag": "flag-intl", "cat": "dna", "repo": "unicity-astrid/book", "desc": "The canonical reference for Astrid OS: kernel, capsules, host ABI, the bus, and the security model.", "lang": "Perl", "stars": "7.5k", "forks": "31"},
    {"date": "Jul 3", "flag": "flag-intl", "cat": "cabinet", "repo": "unicity-astrid/handbook", "desc": "How to work on Astrid: the polyrepo, the kernel-is-dumb law, the RFC trigger, contribution guide.", "lang": None, "stars": "7.5k", "forks": "42"},
    {"date": "Jul 2", "flag": "flag-intl", "cat": "zap", "repo": "shadcn/improve", "desc": "Use your most capable model to audit your codebase and write plans for cheaper models to execute.", "lang": None, "stars": "7.5k", "forks": "313"},
    {"date": "Jul 1", "flag": "flag-us", "cat": "robot", "repo": "omnigent-ai/omnigent", "desc": "Open-source AI agent framework and meta-harness: orchestrate Claude Code, Codex, and more.", "lang": "Python", "stars": "6.7k", "forks": "895"},
    {"date": "Jun 30", "flag": "flag-intl", "cat": "robot", "repo": "cobusgreyling/loop-engineering", "desc": "Practical patterns, starters & CLI tools for loop engineering with AI coding agents.", "lang": "JavaScript", "stars": "6.5k", "forks": "833"},
    {"date": "Jun 29", "flag": "flag-intl", "cat": "robot", "repo": "deepseek-ai/DeepSpec", "desc": "A full-stack codebase for training and evaluating speculative decoding algorithms.", "lang": "Python", "stars": "6.4k", "forks": "566"},
    {"date": "Jun 28", "flag": "flag-us", "cat": "zap", "repo": "diffusionstudio/lottie", "desc": "Generate production-ready Lottie animations with Claude Code or Codex.", "lang": "TypeScript", "stars": "4.6k", "forks": "257"},
    {"date": "Jun 27", "flag": "flag-intl", "cat": "package", "repo": "zhongerxin/Cowart", "desc": "A compact, fast-moving JavaScript toolkit.", "lang": "JavaScript", "stars": "4.1k", "forks": "325"},
    {"date": "Jun 26", "flag": "flag-intl", "cat": "package", "repo": "makerspet/oomwoo", "desc": "Open-source vacuum robot cleaner.", "lang": "Python", "stars": "3.9k", "forks": "180"},
    {"date": "Jun 25", "flag": "flag-intl", "cat": "search", "repo": "bikini/exploitarium", "desc": "A single archive of public exploit PoCs and vulnerability research writeups.", "lang": "Python", "stars": "3.8k", "forks": "1.1k"},
    {"date": "Jun 24", "flag": "flag-intl", "cat": "brain", "repo": "elder-plinius/T3MP3ST", "desc": "Autonomous red teaming platform; multi-agent offensive-security meta-harness.", "lang": "TypeScript", "stars": "3.6k", "forks": "790"},
    {"date": "Jun 23", "flag": "flag-intl", "cat": "brain", "repo": "BuilderIO/skills", "desc": "Skills for coding agents.", "lang": "JavaScript", "stars": "3.5k", "forks": "175"},
    {"date": "Jun 22", "flag": "flag-intl", "cat": "mobile", "repo": "Yu9191/wloc", "desc": "Override Apple network location (gs-loc) coordinates — Surge / Quantumult X / Loon / Stash.", "lang": "JavaScript", "stars": "3.3k", "forks": "473"},
    {"date": "Jun 21", "flag": "flag-intl", "cat": "brain", "repo": "vercel/eve", "desc": "The framework for building agents.", "lang": "TypeScript", "stars": "3.3k", "forks": "270"},
    {"date": "Jun 20", "flag": "flag-intl", "cat": "robot", "repo": "baairon/torlink", "desc": "A sleek, zero-setup torrent finder and downloader that lives right in your terminal.", "lang": "TypeScript", "stars": "3.3k", "forks": "217"},
    {"date": "Jun 19", "flag": "flag-intl", "cat": "robot", "repo": "Waishnav/devspace", "desc": "Turn ChatGPT into Codex, or turn Claude web into Claude Code.", "lang": "TypeScript", "stars": "3.1k", "forks": "322"},
    {"date": "Jun 18", "flag": "flag-intl", "cat": "zap", "repo": "bozhouDev/codex-orange-book", "desc": "A full end-to-end unofficial guide to Codex, install to real-world case studies.", "lang": "HTML", "stars": "2.7k", "forks": "269"},
    {"date": "Jun 17", "flag": "flag-intl", "cat": "globe", "repo": "tamnd/kage", "desc": "Shadow any website for offline viewing, with the JavaScript stripped out.", "lang": "Go", "stars": "2.7k", "forks": "99"},
    {"date": "Jun 16", "flag": "flag-intl", "cat": "robot", "repo": "Forward-Future/loopy", "desc": "A library of practical AI-agent loops and an installable skill for finding and adapting them.", "lang": "JavaScript", "stars": "2.5k", "forks": "216"},
    {"date": "Jun 15", "flag": "flag-intl", "cat": "robot", "repo": "JimLiu/baoyu-design", "desc": "Run Claude Design locally as an Agent Skill — Cursor, Claude Code & more.", "lang": "JavaScript", "stars": "2.5k", "forks": "184"},
    {"date": "Jun 14", "flag": "flag-intl", "cat": "robot", "repo": "vorssaint/vorssaint-utils", "desc": "Free open-source macOS menu bar toolkit — volume mixer, system monitor, dock preview.", "lang": "Swift", "stars": "2.5k", "forks": "92"},
    {"date": "Jun 13", "flag": "flag-sg", "cat": "brain", "repo": "cloudflare/security-audit-skill", "desc": "A coding-agent skill for multi-phase security audits with independently verified findings.", "lang": "JavaScript", "stars": "2.3k", "forks": "170"},
    {"date": "Jun 12", "flag": "flag-us", "cat": "robot", "repo": "TestSprite/testsprite-cli", "desc": "Official TestSprite CLI — AI-powered automated testing from your terminal.", "lang": "TypeScript", "stars": "2.2k", "forks": "79"},
    {"date": "Jun 11", "flag": "flag-intl", "cat": "robot", "repo": "lenucksi/aur-malware-check", "desc": "Detection tools for the June 2026 atomic-lockfile AUR supply-chain attack.", "lang": "Python", "stars": "2.0k", "forks": "44"},
    {"date": "Jun 10", "flag": "flag-intl", "cat": "robot", "repo": "shy3130/tickflow-stock-panel", "desc": "Self-hosted, zero-ops A-share stock picking, monitoring and backtesting workbench.", "lang": "TypeScript", "stars": "1.9k", "forks": "376"},
    {"date": "Jun 9", "flag": "flag-intl", "cat": "brain", "repo": "davidondrej/skills", "desc": "Access to David Ondrej's personal agent skills.", "lang": None, "stars": "1.9k", "forks": "245"},
]

TRENDING = [
    {"flag": "flag-intl", "repo": "elder-plinius/T3MP3ST", "desc": "Autonomous red teaming platform; multi-agent offensive-security meta-harness.", "lang": "TypeScript", "stars": "3,535", "forks": "786"},
    {"flag": "flag-us", "repo": "synthetic-sciences/openscience", "desc": "The open-source AI workbench for scientific research.", "lang": "TypeScript", "stars": "1,547", "forks": "216"},
    {"flag": "flag-intl", "repo": "ammaarreshi/Generals-Mac-iOS-iPad", "desc": "Command & Conquer Generals: Zero Hour running natively on macOS, iPhone & iPad.", "lang": "C++", "stars": "1,317", "forks": "105"},
]

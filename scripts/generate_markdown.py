#!/usr/bin/env python3
"""Generate the searchable skill list source page from data/skills.json."""
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
CATEGORY_NAMES = {
    "coding": "Coding", "research": "Research", "writing": "Writing",
    "data": "Data & Automation", "devops": "DevOps", "creative": "Creative", "other": "Other",
}
LOCALES = {
    "en": {"name": "English", "title": "Awesome Agent Skills", "updated": "Last updated", "total": "Total skills", "intro": "A curated list of reusable skills for Codex, Claude Code, Cursor, OpenCode, and other AI coding agents.", "categories": "Categories", "contributing": "Contributing", "contribute_text": "Add a quality, reusable Agent Skill by opening a pull request."},
    "zh": {"name": "简体中文", "title": "优秀 AI Agent Skills", "updated": "最后更新", "total": "Skill 总数", "intro": "为 Codex、Claude Code、Cursor、OpenCode 及其他 AI 编程 Agent 精选的可复用 Skill。", "categories": "分类", "contributing": "参与贡献", "contribute_text": "欢迎通过 Pull Request 提交高质量、可复用的 Agent Skill。"},
    "fr": {"name": "Français", "title": "Skills d'agents IA remarquables", "updated": "Dernière mise à jour", "total": "Skills au total", "intro": "Une sélection de skills réutilisables pour Codex, Claude Code, Cursor, OpenCode et d'autres agents de programmation IA.", "categories": "Catégories", "contributing": "Contribuer", "contribute_text": "Ajoutez un skill d'agent de qualité et réutilisable avec une pull request."},
    "ja": {"name": "日本語", "title": "優れた AI エージェントスキル", "updated": "最終更新", "total": "スキル数", "intro": "Codex、Claude Code、Cursor、OpenCode などの AI コーディングエージェント向けの再利用可能なスキル集です。", "categories": "カテゴリ", "contributing": "貢献", "contribute_text": "高品質で再利用可能なエージェントスキルを Pull Request で追加してください。"},
    "ru": {"name": "Русский", "title": "Отличные навыки ИИ-агентов", "updated": "Последнее обновление", "total": "Всего навыков", "intro": "Подборка повторно используемых навыков для Codex, Claude Code, Cursor, OpenCode и других ИИ-агентов программирования.", "categories": "Категории", "contributing": "Участие", "contribute_text": "Добавьте качественный повторно используемый навык агента через pull request."},
    "es": {"name": "Español", "title": "Skills destacados para agentes de IA", "updated": "Última actualización", "total": "Skills en total", "intro": "Una lista seleccionada de skills reutilizables para Codex, Claude Code, Cursor, OpenCode y otros agentes de programación con IA.", "categories": "Categorías", "contributing": "Contribuir", "contribute_text": "Añade un skill de agente reutilizable y de calidad mediante una pull request."},
    "hi": {"name": "हिन्दी", "title": "उत्कृष्ट AI एजेंट स्किल्स", "updated": "अंतिम अपडेट", "total": "कुल स्किल्स", "intro": "Codex, Claude Code, Cursor, OpenCode और अन्य AI कोडिंग एजेंटों के लिए पुन: उपयोग योग्य स्किल्स की चुनी हुई सूची।", "categories": "श्रेणियाँ", "contributing": "योगदान", "contribute_text": "पुल रिक्वेस्ट के माध्यम से एक उच्च-गुणवत्ता, पुन: उपयोग योग्य एजेंट स्किल जोड़ें।"},
    "ar": {"name": "العربية", "title": "مهارات مميزة لوكلاء الذكاء الاصطناعي", "updated": "آخر تحديث", "total": "إجمالي المهارات", "intro": "قائمة منتقاة من المهارات القابلة لإعادة الاستخدام لـ Codex وClaude Code وCursor وOpenCode وغيرها من وكلاء البرمجة بالذكاء الاصطناعي.", "categories": "الفئات", "contributing": "المساهمة", "contribute_text": "أضف مهارة وكيل عالية الجودة وقابلة لإعادة الاستخدام عبر طلب سحب."},
    "pt": {"name": "Português", "title": "Skills incríveis para agentes de IA", "updated": "Última atualização", "total": "Total de skills", "intro": "Uma lista selecionada de skills reutilizáveis para Codex, Claude Code, Cursor, OpenCode e outros agentes de programação com IA.", "categories": "Categorias", "contributing": "Contribuir", "contribute_text": "Adicione um skill de agente reutilizável e de qualidade por meio de uma pull request."},
    "bn": {"name": "বাংলা", "title": "চমৎকার AI এজেন্ট স্কিল", "updated": "সর্বশেষ হালনাগাদ", "total": "মোট স্কিল", "intro": "Codex, Claude Code, Cursor, OpenCode এবং অন্যান্য AI কোডিং এজেন্টের জন্য পুনর্ব্যবহারযোগ্য স্কিলের নির্বাচিত তালিকা।", "categories": "বিভাগ", "contributing": "অবদান", "contribute_text": "পুল রিকোয়েস্টের মাধ্যমে একটি মানসম্মত, পুনর্ব্যবহারযোগ্য এজেন্ট স্কিল যোগ করুন।"},
    "de": {"name": "Deutsch", "title": "Ausgezeichnete KI-Agent-Skills", "updated": "Letzte Aktualisierung", "total": "Skills insgesamt", "intro": "Eine kuratierte Liste wiederverwendbarer Skills für Codex, Claude Code, Cursor, OpenCode und andere KI-Programmieragenten.", "categories": "Kategorien", "contributing": "Mitwirken", "contribute_text": "Füge einen hochwertigen, wiederverwendbaren Agent-Skill per Pull Request hinzu."},
    "ko": {"name": "한국어", "title": "훌륭한 AI 에이전트 스킬", "updated": "마지막 업데이트", "total": "전체 스킬", "intro": "Codex, Claude Code, Cursor, OpenCode 및 기타 AI 코딩 에이전트를 위한 재사용 가능한 스킬 모음입니다.", "categories": "카테고리", "contributing": "기여", "contribute_text": "고품질의 재사용 가능한 에이전트 스킬을 Pull Request로 추가해 주세요."},
    "tr": {"name": "Türkçe", "title": "Harika yapay zeka ajan becerileri", "updated": "Son güncelleme", "total": "Toplam beceri", "intro": "Codex, Claude Code, Cursor, OpenCode ve diğer yapay zeka kodlama ajanları için yeniden kullanılabilir becerilerden oluşan seçilmiş bir liste.", "categories": "Kategoriler", "contributing": "Katkıda bulun", "contribute_text": "Kaliteli, yeniden kullanılabilir bir ajan becerisini pull request ile ekleyin."},
    "id": {"name": "Bahasa Indonesia", "title": "Skill agen AI terbaik", "updated": "Pembaruan terakhir", "total": "Total skill", "intro": "Daftar terpilih skill yang dapat digunakan kembali untuk Codex, Claude Code, Cursor, OpenCode, dan agen pemrograman AI lainnya.", "categories": "Kategori", "contributing": "Berkontribusi", "contribute_text": "Tambahkan skill agen yang berkualitas dan dapat digunakan kembali melalui pull request."},
}


def date(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return str(value)[:10]


def render(source, groups, locale):
    lines = [f"# {locale['title']}", "", f"> {locale['updated']}: **{date(source.get('last_updated', ''))}** | {locale['total']}: **{source.get('total', 0)}**", "", locale["intro"], ""]
    if groups:
        lines += [f"## {locale['categories']}", ""] + [f"- [{CATEGORY_NAMES.get(key, key.title())}](#{key})" for key in sorted(groups)] + ["", "---", ""]
    for key in sorted(groups):
        lines += [f"## {CATEGORY_NAMES.get(key, key.title())}", ""]
        for index, skill in enumerate(sorted(groups[key], key=lambda item: item.get("stars", 0), reverse=True), 1):
            lines += [f"### {index}. [{skill['name']}]({skill['url']})", "", f"⭐ **{skill.get('stars', 0):,}** | 🔤 **{skill.get('language', 'N/A')}** | 📅 **{date(skill.get('updated_at', ''))}**", "", skill.get("description", "").strip(), ""]
            if skill.get("topics"):
                lines += ["**Tags:** " + " ".join(f"`{tag}`" for tag in skill["topics"][:8]), ""]
            lines += ["---", ""]
    lines += [f"## {locale['contributing']}", "", f"{locale['contribute_text']} See [CONTRIBUTING.md](../../CONTRIBUTING.md).", ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    source = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))
    groups = {}
    for skill in source.get("skills", []):
        groups.setdefault(skill.get("category", "other"), []).append(skill)
    for code, locale in LOCALES.items():
        target = ROOT / "docs" / code / "projects.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(source, groups, locale), encoding="utf-8")
    shutil.copyfile(ROOT / "data/skills.json", ROOT / "docs/data/skills.json")
    print(f"Generated {len(LOCALES)} language directories")


if __name__ == "__main__":
    main()

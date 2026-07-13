from pathlib import Path

from .generator import JournalEntry


def format_markdown(entry: JournalEntry) -> str:
    return (
        f"# Sol {entry['sol']:04d}: {entry['title']}\n\n"
        f"{entry['opening']}\n\n"
        f"{entry['citizen_story']}\n\n"
        f"{entry['impact']}\n\n"
        f"{entry['future_implication']}\n"
    )


def format_social_draft(entry: JournalEntry) -> str:
    citizens = ", ".join(entry["citizens"]) or "the citizens of Ares Alpha"
    return (
        f"Sol {entry['sol']:04d} — {entry['title']}\n\n"
        f"{entry['opening']} {citizens} helped shape the day.\n\n"
        f"{entry['impact']} {entry['future_implication']}\n"
    )


def export_chronicle(
    entry: JournalEntry, output_root: Path | str = "."
) -> dict[str, Path]:
    root = Path(output_root)
    filename = f"sol-{entry['sol']:04d}"
    markdown_path = root / "docs" / "chronicles" / f"{filename}.md"
    social_path = root / "social" / "x" / f"{filename}.txt"
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    social_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(format_markdown(entry), encoding="utf-8")
    social_path.write_text(format_social_draft(entry), encoding="utf-8")
    return {"markdown": markdown_path, "social": social_path}

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path

from scraper import scrape_job
from analyzer import parse_jd, score_resume, draft_cover_letter
from tracker import log_application, save_cover_letter

app = typer.Typer()
console = Console()

RESUME_FILE = "resume.txt"


def load_resume() -> str:
    if not Path(RESUME_FILE).exists():
        console.print(f"[red]Error:[/red] {RESUME_FILE} not found. Create it in the project root.")
        raise typer.Exit(1)
    return Path(RESUME_FILE).read_text(encoding="utf-8")


@app.command()
def analyze(
    url: str = typer.Argument(..., help="Job posting URL"),
    skip_cover_letter: bool = typer.Option(False, "--no-cl", help="Skip cover letter generation"),
):
    """Analyze a job posting against your resume and log the result."""

    console.print(Panel("[bold cyan]Job Application Tracker[/bold cyan]", subtitle="Powered by Gemini"))

    # Step 1: Scrape
    console.print("\n[yellow]Scraping job posting...[/yellow]")
    try:
        jd_text = scrape_job(url)
        console.print(f"[green]Scraped {len(jd_text)} characters[/green]")
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    # Step 2: Load resume
    resume_text = load_resume()

    # Step 3: Parse JD
    console.print("[yellow]Parsing job description...[/yellow]")
    parsed = parse_jd(jd_text)

    jd_table = Table(show_header=False, box=None, padding=(0, 1))
    for key, value in parsed.items():
        jd_table.add_row(f"[bold]{key}[/bold]", value)
    console.print(Panel(jd_table, title="Job Details"))

    # Step 4: Score resume
    console.print("[yellow]Scoring your resume...[/yellow]")
    score = score_resume(jd_text, resume_text)

    score_table = Table(show_header=False, box=None, padding=(0, 1))
    for key, value in score.items():
        color = "green" if key == "Score" else "white"
        score_table.add_row(f"[bold]{key}[/bold]", f"[{color}]{value}[/{color}]")
    console.print(Panel(score_table, title="Resume Match Analysis"))

    # Step 5: Cover letter
    cover_letter_path = "N/A"
    if not skip_cover_letter:
        console.print("[yellow]Drafting cover letter...[/yellow]")
        cover_letter = draft_cover_letter(jd_text, resume_text, parsed)
        cover_letter_path = save_cover_letter(
            parsed.get("Company", "company"),
            parsed.get("Role", "role"),
            cover_letter
        )
        console.print(Panel(cover_letter, title="Cover Letter Draft"))
        console.print(f"[green]Saved to:[/green] {cover_letter_path}")

    # Step 6: Log
    log_application(url, parsed, score, cover_letter_path)
    console.print("\n[bold green]Logged to logs/applications.csv[/bold green]")


@app.command()
def history():
    """Show all logged applications."""
    import csv
    log_file = "logs/applications.csv"
    if not Path(log_file).exists():
        console.print("[yellow]No applications logged yet.[/yellow]")
        raise typer.Exit()

    with open(log_file, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        console.print("[yellow]No applications yet.[/yellow]")
        return

    table = Table(title="Application History")
    for col in ["Date", "Company", "Role", "Match Score", "Verdict"]:
        table.add_column(col)

    for row in rows:
        score = row.get("Match Score", "N/A")
        color = "green" if score.isdigit() and int(score) >= 7 else "yellow" if score.isdigit() and int(score) >= 5 else "red"
        table.add_row(
            row["Date"],
            row["Company"],
            row["Role"],
            f"[{color}]{score}/10[/{color}]",
            row["Verdict"],
        )

    console.print(table)


if __name__ == "__main__":
    app()

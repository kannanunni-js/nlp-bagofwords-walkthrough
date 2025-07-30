from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box


def print_project_banner(
    project_title: str,
    description: str,
    features: list[str],
    repo_name: str,
    repo_link: str,
):
    console = Console()

    # Repository info in its own table to allow proper wrapping
    repo_table = Table.grid(padding=(0, 1))
    repo_table.add_column(style="bold green", justify="right")
    repo_table.add_column(style="cyan", overflow="fold")  # allow wrapping
    repo_table.add_row("Repository:", f"{repo_name}")
    repo_table.add_row("Link:", f"[u blue]{repo_link}[/]")  # underlined clickable style

    # Intro text and features
    feature_list = "\n".join(f"- {feature}" for feature in features)
    intro_text = f"{description.strip()}\n\n[b]Features:[/b]\n{feature_list}"
    intro_message = Text.from_markup(intro_text)

    # Main message layout
    layout = Table.grid(expand=True)
    layout.add_column(ratio=3)
    layout.add_column(ratio=2)
    layout.add_row(intro_message, repo_table)

    # Print final panel
    console.print(
        Panel(
            layout,
            box=box.ROUNDED,
            padding=(1, 2),
            title=f"[b red]{project_title} 📰🔍",
            border_style="bright_blue",
        ),
        justify="center",
    )

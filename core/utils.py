from pathlib import Path


def bootcheck() -> None:
    """Ensure required directories exist on startup."""
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print("Bootcheck passed.")

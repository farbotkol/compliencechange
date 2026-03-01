"""Command-line interface for compliance monitoring."""
import sys

from app.collectors.australia import AustraliaCollector
from app.collectors.european_union import EuropeanUnionCollector
from app.collectors.international import InternationalCollector
from app.collectors.united_kingdom import UnitedKingdomCollector
from app.collectors.united_states import UnitedStatesCollector
from app.db import complete_scan_run, create_scan_run, get_db_session, save_compliance_change
from app.models import init_db


def run_scan():
    """Run a compliance scan across all collectors."""
    print("Starting compliance scan...")

    # Initialize database
    init_db()
    session = get_db_session()

    # Create scan run
    scan_run = create_scan_run(session)
    print(f"Created scan run {scan_run.id}")

    # Initialize collectors
    collectors = [
        AustraliaCollector(),
        EuropeanUnionCollector(),
        UnitedKingdomCollector(),
        UnitedStatesCollector(),
        InternationalCollector(),
    ]

    items_found = 0
    failures = []

    # Run each collector
    for collector in collectors:
        collector_name = collector.__class__.__name__
        print(f"\nRunning {collector_name}...")

        try:
            changes = collector.collect()
            print(f"  Found {len(changes)} potential changes")

            for change_data in changes:
                saved = save_compliance_change(session, change_data)
                if saved:
                    items_found += 1
                    print(f"  ✓ Saved: {change_data.title[:60]}...")
                else:
                    print(f"  - Skipped (duplicate): {change_data.title[:60]}...")

        except Exception as e:
            error_msg = f"{collector_name}: {str(e)}"
            failures.append(error_msg)
            print(f"  ✗ Error: {e}")

    # Complete scan run
    failure_text = "; ".join(failures) if failures else None
    complete_scan_run(session, scan_run.id, items_found, failure_text)

    print(f"\n{'='*60}")
    print("Scan completed!")
    print(f"  Items found: {items_found}")
    print(f"  Failures: {len(failures)}")
    if failures:
        for failure in failures:
            print(f"    - {failure}")
    print(f"{'='*60}")

    session.close()


def init_database():
    """Initialize the database."""
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m app.cli <command>")
        print("Commands:")
        print("  run-scan    - Run a compliance scan")
        print("  init-db     - Initialize the database")
        sys.exit(1)

    command = sys.argv[1]

    if command == "run-scan":
        run_scan()
    elif command == "init-db":
        init_database()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

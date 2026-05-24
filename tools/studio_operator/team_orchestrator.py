#!/usr/bin/env python3
"""
Team Orchestrator for Roblox Tower Defense Prototype

Provides unified status, planning, and review workflows for team development.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class TeamOrchestrator:
    def __init__(self):
        self.script_dir = Path(__file__).resolve().parent
        self.project_root = self.script_dir.parent.parent
        self.docs_dir = self.project_root / "docs" / "team"
        self.logs_dir = self.project_root / "logs"

    def run_command(self, cmd, capture=True):
        """Run a shell command and return output."""
        try:
            if capture:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=str(self.project_root)
                )
                return result.stdout.strip(), result.returncode
            else:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=str(self.project_root)
                )
                return "", result.returncode
        except Exception as e:
            return str(e), 1

    def status(self):
        """Check team status."""
        print("=== Team Status ===\n")

        # Git status
        print("[Git Status]")
        branch, _ = self.run_command("git branch --show-current")
        status, _ = self.run_command("git status --short")
        commits, _ = self.run_command("git log --oneline -3")

        print(f"Branch: {branch}")
        if status:
            lines = status.split('\n')
            print(f"Uncommitted changes: {len([l for l in lines if l])} files")
        else:
            print("Working tree: Clean")
        print("Recent commits:")
        for line in commits.split('\n')[:3]:
            if line:
                print(f"  {line}")

        # PR status
        print("\n[Pull Requests]")
        prs, _ = self.run_command("gh pr list --state open --json number,title")
        if prs:
            try:
                pr_list = json.loads(prs)
                print(f"Open PRs: {len(pr_list)}")
                for pr in pr_list[:5]:
                    print(f"  #{pr['number']} - {pr['title']}")
            except:
                print("Could not parse PR list")
        else:
            print("Open PRs: 0")

        # Game state
        print("\n[Game State]")
        state_file = self.docs_dir / "CURRENT_STATE.md"
        if state_file.exists():
            print("Current state documented in: docs/team/CURRENT_STATE.md")
            with open(state_file) as f:
                content = f.read()
                features = [l for l in content.split('\n') if l.startswith('- ✅')]
                print("Features implemented:")
                for feature in features[:5]:
                    print(f"  {feature}")
        else:
            print("State file not found")

        # Build status
        print("\n[Build Status]")
        build_path = self.project_root / "build" / "game.rbxlx"
        if build_path.exists():
            size_mb = build_path.stat().st_size / (1024 * 1024)
            mtime = datetime.fromtimestamp(build_path.stat().st_mtime)
            print(f"Build exists: Yes")
            print(f"Build date: {mtime}")
            print(f"Build size: {size_mb:.2f} MB")
        else:
            print("Build exists: No")

        # Test status
        print("\n[Test Status]")
        report_path = self.logs_dir / "demo_test_report.md"
        if report_path.exists():
            mtime = datetime.fromtimestamp(report_path.stat().st_mtime)
            print(f"Last test: {mtime}")
            with open(report_path) as f:
                for line in f:
                    if "Status:" in line:
                        print(f"Last status: {line.strip()}")
                        break
        else:
            print("No test report found")

        print("\n=== End Status ===")

    def plan_next(self):
        """Plan next tasks."""
        print("=== Team Plan: Next Tasks ===\n")

        next_file = self.docs_dir / "NEXT_ACTIONS.md"
        if next_file.exists():
            print("Next 5 Tasks (from NEXT_ACTIONS.md):\n")
            with open(next_file) as f:
                content = f.read()
                tasks = content.split("### Task ")
                for i, task in enumerate(tasks[1:6], 1):
                    lines = task.split('\n')
                    title = lines[0].replace(':', '').strip()
                    priority = next((l for l in lines if 'Priority:' in l), "Unknown")
                    effort = next((l for l in lines if 'Effort:' in l), "Unknown")

                    print(f"[{i}] {title}")
                    print(f"  {priority}")
                    print(f"  {effort}\n")
        else:
            print("NEXT_ACTIONS.md not found")

        print("=== End Plan ===")
        print("\nFor detailed planning, see: docs/team/NEXT_ACTIONS.md")

    def review_demo(self):
        """Review demo test results."""
        print("=== Team Review: Demo Test ===\n")

        report_path = self.logs_dir / "demo_test_report.md"
        if report_path.exists():
            print("Test Report:\n")
            with open(report_path) as f:
                lines = f.readlines()
                for line in lines[:30]:
                    print(line, end='')
            print("\n... (see full report in logs/demo_test_report.md)")
        else:
            print("Test report not found")

        # Check for videos
        recordings_dir = self.logs_dir / "recordings"
        if recordings_dir.exists():
            videos = sorted(
                recordings_dir.glob("*.mp4"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            if videos:
                print(f"\nLatest recording: {videos[0].name}")

        print("\n=== End Review ===")

    def dry_run(self):
        """Run dry build without Studio."""
        print("=== Team Dry Run: Build Only ===\n")

        print("Building game...")
        _, code = self.run_command(
            f"powershell -NoProfile -Command \"& '{self.project_root}/scripts/build_place.ps1'\"",
            capture=False
        )

        build_path = self.project_root / "build" / "game.rbxlx"
        if build_path.exists() and code == 0:
            size_mb = build_path.stat().st_size / (1024 * 1024)
            print(f"\n✅ Build successful!")
            print(f"Build size: {size_mb:.2f} MB")
            print(f"Build path: {build_path}")
        else:
            print(f"\n❌ Build failed!")
            return 1

        print("\n=== End Dry Run ===")
        print("\nBuild verified. Ready for demo test or merge.")
        return 0

    def cycle(self, skip_demo=False):
        """Run full development cycle."""
        print("=== Team Cycle: Full Development Workflow ===\n")

        # Step 1: Status
        print("[Step 1/4] Checking team status...")
        self.status()

        # Step 2: Plan
        print("\n[Step 2/4] Planning next tasks...")
        self.plan_next()

        # Step 3: Dry Run
        print("\n[Step 3/4] Running dry build...")
        if self.dry_run() != 0:
            print("\n❌ Build failed. Cycle stopped.")
            return 1

        # Step 4: Demo (optional)
        if not skip_demo:
            print("\n[Step 4/4] Running demo test...")
            self.review_demo()
        else:
            print("\n[Step 4/4] Skipping demo test (--skip-demo flag)")

        print("\n=== Cycle Complete ===")
        print("\nNext steps:")
        print("  1. Review test results")
        print("  2. If approved: Run pr_safe_merge.ps1")
        print("  3. If issues: Fix and re-run cycle")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Team Orchestrator for Roblox Tower Defense Prototype"
    )
    parser.add_argument(
        "--action",
        choices=["status", "plan_next", "review_demo", "dry_run", "cycle"],
        default="status",
        help="Action to perform"
    )
    parser.add_argument(
        "--skip-demo",
        action="store_true",
        help="Skip demo test in cycle"
    )

    args = parser.parse_args()

    orchestrator = TeamOrchestrator()

    if args.action == "status":
        orchestrator.status()
    elif args.action == "plan_next":
        orchestrator.plan_next()
    elif args.action == "review_demo":
        orchestrator.review_demo()
    elif args.action == "dry_run":
        return orchestrator.dry_run()
    elif args.action == "cycle":
        return orchestrator.cycle(skip_demo=args.skip_demo)

    return 0


if __name__ == "__main__":
    sys.exit(main())

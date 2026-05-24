#!/usr/bin/env python3
"""
Model Router for Roblox Tower Defense Prototype

Analyzes tasks and recommends appropriate AI model or Codex profile.
"""

import argparse
import sys
from pathlib import Path


class ModelRouter:
    def __init__(self):
        self.script_dir = Path(__file__).resolve().parent
        self.project_root = self.script_dir.parent.parent

    def analyze_task(self, task_description):
        """Analyze task and recommend model."""
        task_lower = task_description.lower()

        # Keywords for each level
        quick_keywords = [
            "readme", "documentation", "update doc", "status", "prompt",
            "script", "ps1", "summary", "list", "show", "check status",
            "team_status", "team_plan_next", "dry_run", "summarize"
        ]

        code_keywords = [
            "lua", "implement", "feature", "add", "fix", "bug", "service",
            "config", "tower", "enemy", "economy", "wave", "map", "path",
            "client", "server", "refactor", "test", "unit test", "pr review",
            "normal pr", "small refactor", "single file", "single service"
        ]

        deep_keywords = [
            "architecture", "design", "security", "merge", "pr manager",
            "process manager", "auto-merge", "race condition", "debug",
            "complex", "hard", "cross-file", "cross-service", "refactor",
            "version upgrade", "performance", "conflict", "risky"
        ]

        verify_keywords = [
            "build", "verify", "check", "review", "log", "demo", "test",
            "regression", "smoke test", "report", "analyze"
        ]

        # Count keyword matches
        quick_score = sum(1 for kw in quick_keywords if kw in task_lower)
        code_score = sum(1 for kw in code_keywords if kw in task_lower)
        deep_score = sum(1 for kw in deep_keywords if kw in task_lower)
        verify_score = sum(1 for kw in verify_keywords if kw in task_lower)

        # Determine mode
        scores = {
            "quick": quick_score,
            "code": code_score,
            "deep": deep_score,
            "verify": verify_score
        }

        # Deep tasks override others
        if deep_score > 0:
            mode = "deep"
        elif verify_score > code_score and verify_score > quick_score:
            mode = "verify"
        elif code_score > quick_score:
            mode = "code"
        elif quick_score > 0:
            mode = "quick"
        else:
            # Default to code if no keywords match
            mode = "code"

        return mode, scores

    def get_model_info(self, mode):
        """Get model and profile info for mode."""
        models = {
            "quick": {
                "claude": "haiku",
                "codex": "quick",
                "cost": "Lowest",
                "speed": "Fastest",
                "reasoning": "Basic"
            },
            "code": {
                "claude": "sonnet",
                "codex": "code",
                "cost": "Medium",
                "speed": "Medium",
                "reasoning": "Strong"
            },
            "deep": {
                "claude": "opusplan",
                "codex": "deep",
                "cost": "Highest",
                "speed": "Slowest",
                "reasoning": "Maximum"
            },
            "verify": {
                "claude": "sonnet",
                "codex": "verify",
                "cost": "Low-Medium",
                "speed": "Fast-Medium",
                "reasoning": "Focused"
            }
        }
        return models.get(mode, models["code"])

    def get_reason(self, mode, task_description):
        """Get explanation for recommendation."""
        reasons = {
            "quick": "Documentation or status task with no code changes or risk",
            "code": "Code implementation with clear scope and moderate complexity",
            "deep": "Complex task requiring deep reasoning for safety or architecture",
            "verify": "Verification or analysis task with focused scope"
        }
        return reasons.get(mode, "Task analysis complete")

    def recommend(self, task_description):
        """Get full recommendation."""
        mode, scores = self.analyze_task(task_description)
        model_info = self.get_model_info(mode)
        reason = self.get_reason(mode, task_description)

        return {
            "task": task_description,
            "recommended_mode": mode,
            "claude_model": model_info["claude"],
            "codex_profile": model_info["codex"],
            "cost": model_info["cost"],
            "speed": model_info["speed"],
            "reasoning": model_info["reasoning"],
            "reason": reason,
            "scores": scores
        }

    def print_recommendation(self, rec):
        """Print recommendation in user-friendly format."""
        print("\n" + "=" * 60)
        print("MODEL ROUTING RECOMMENDATION")
        print("=" * 60)

        print(f"\nTask: {rec['task']}")
        print(f"\nRecommended Mode: {rec['recommended_mode'].upper()}")
        print(f"Claude Model: {rec['claude_model']}")
        print(f"Codex Profile: {rec['codex_profile']}")
        print(f"\nCharacteristics:")
        print(f"  Cost: {rec['cost']}")
        print(f"  Speed: {rec['speed']}")
        print(f"  Reasoning: {rec['reasoning']}")

        print(f"\nReason: {rec['reason']}")

        print(f"\nSafe Commands:")
        print(f"  Claude:  claude --model {rec['claude_model']}")
        print(f"  Codex:   codex --profile {rec['codex_profile']}")

        print("\n" + "=" * 60)

    def print_table(self):
        """Print mode comparison table."""
        print("\n" + "=" * 100)
        print("MODEL ROUTING LEVELS")
        print("=" * 100)

        modes = ["quick", "code", "deep", "verify"]
        print(f"\n{'Mode':<10} {'Claude':<12} {'Codex':<10} {'Cost':<12} {'Speed':<10} {'Reasoning':<15}")
        print("-" * 100)

        for mode in modes:
            info = self.get_model_info(mode)
            print(f"{mode:<10} {info['claude']:<12} {info['codex']:<10} {info['cost']:<12} {info['speed']:<10} {info['reasoning']:<15}")

        print("\n" + "=" * 100)
        print("\nQuick:  Documentation, status, simple scripts")
        print("Code:   Feature implementation, bug fixes, single-service changes")
        print("Deep:   Architecture, security, risky operations, PR manager changes")
        print("Verify: Log analysis, build checks, test reviews")
        print("\n" + "=" * 100)

    def print_explain(self):
        """Print explanation of routing system."""
        print("\n" + "=" * 60)
        print("MODEL ROUTING SYSTEM")
        print("=" * 60)

        print("""
The model routing system helps you choose the right AI model for each task.

LEVELS:
  quick  - Fast, cheap, for docs and status (haiku)
  code   - Balanced, for code implementation (sonnet)
  deep   - Powerful, for complex tasks (opus/opusplan)
  verify - Focused, for testing and review (haiku/sonnet)

DECISION:
  1. Is it documentation? -> quick
  2. Is it code implementation? -> code
  3. Is it verification? -> verify
  4. Is it risky/complex? -> deep

RULES:
  - Never use quick for risky operations
  - Never use quick for PR manager changes
  - Always use deep for architecture
  - Always use deep for merge safety
  - Use code for normal feature work

COMMANDS:
  model_recommend.ps1 -Task "your task"
  claude --model haiku/sonnet/opusplan
  codex --profile quick/code/deep/verify

For more info: see docs/team/MODEL_ROUTING.md
        """)

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Model Router - Recommend AI model for tasks"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Task description to analyze"
    )
    parser.add_argument(
        "--mode",
        choices=["explain", "table"],
        help="Show explanation or comparison table"
    )

    args = parser.parse_args()

    router = ModelRouter()

    if args.mode == "explain":
        router.print_explain()
    elif args.mode == "table":
        router.print_table()
    elif args.task:
        rec = router.recommend(args.task)
        router.print_recommendation(rec)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

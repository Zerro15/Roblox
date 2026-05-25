"""Inspect the built Roblox place XML structure.

This tool is intentionally read-only. It verifies that Rojo produced the
expected ServerScriptService layout without launching Roblox Studio.
"""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_PLACE = PROJECT_ROOT / "build" / "game.rbxlx"
DEFAULT_REPORT = PROJECT_ROOT / "logs" / "place_structure_report.md"


def _item_name(item: ET.Element) -> str:
    properties = item.find("Properties")
    if properties is None:
        return ""
    for prop in properties:
        if prop.attrib.get("name") == "Name":
            return prop.text or ""
    return ""


def _string_property(item: ET.Element, prop_name: str) -> str | None:
    properties = item.find("Properties")
    if properties is None:
        return None
    for prop in properties:
        if prop.attrib.get("name") == prop_name:
            return prop.text or ""
    return None


def _bool_property(item: ET.Element, prop_name: str) -> bool | None:
    value = _string_property(item, prop_name)
    if value is None:
        return None
    return value.strip().lower() == "true"


def _find_child(parent: ET.Element, class_name: str | None = None, name: str | None = None) -> ET.Element | None:
    for child in parent.findall("Item"):
        if class_name is not None and child.attrib.get("class") != class_name:
            continue
        if name is not None and _item_name(child) != name:
            continue
        return child
    return None


def _find_item(root: ET.Element, class_name: str | None = None, name: str | None = None) -> ET.Element | None:
    for item in root.iter("Item"):
        if class_name is not None and item.attrib.get("class") != class_name:
            continue
        if name is not None and _item_name(item) != name:
            continue
        return item
    return None


def _child_summary(parent: ET.Element | None) -> list[dict[str, str]]:
    if parent is None:
        return []
    return [
        {
            "class": child.attrib.get("class", ""),
            "name": _item_name(child),
        }
        for child in parent.findall("Item")
    ]


def inspect_place(place_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "place_path": str(place_path),
        "place_exists": place_path.exists(),
        "server_script_service_exists": False,
        "main_exists": False,
        "main_class": None,
        "main_has_source": False,
        "main_source_length": 0,
        "main_disabled": None,
        "services_exists": False,
        "services_relation": "missing",
        "services_children": [],
        "server_script_service_children": [],
        "errors": [],
    }

    if not place_path.exists():
        result["errors"].append("Place file does not exist.")
        return result

    try:
        root = ET.parse(place_path).getroot()
    except ET.ParseError as exc:
        result["errors"].append(f"XML parse failed: {exc}")
        return result

    server_script_service = _find_item(root, "ServerScriptService", "ServerScriptService")
    result["server_script_service_exists"] = server_script_service is not None
    result["server_script_service_children"] = _child_summary(server_script_service)

    if server_script_service is None:
        return result

    main = _find_child(server_script_service, "Script", "Main")
    services = _find_child(server_script_service, "Folder", "services")
    result["main_exists"] = main is not None
    result["services_exists"] = services is not None
    result["services_relation"] = "sibling_of_main" if main is not None and services is not None else "missing"
    result["services_children"] = _child_summary(services)

    if main is not None:
        result["main_class"] = main.attrib.get("class")
        source = _string_property(main, "Source") or ""
        result["main_has_source"] = bool(source.strip())
        result["main_source_length"] = len(source)
        result["main_disabled"] = _bool_property(main, "Disabled")

    return result


def write_report(result: dict[str, Any], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Place Structure Report",
        "",
        f"- place: `{result['place_path']}`",
        f"- place exists: `{result['place_exists']}`",
        f"- ServerScriptService exists: `{result['server_script_service_exists']}`",
        f"- Main exists as Script: `{result['main_exists'] and result['main_class'] == 'Script'}`",
        f"- Main has Source: `{result['main_has_source']}`",
        f"- Main Source length: `{result['main_source_length']}`",
        f"- Main Disabled: `{result['main_disabled']}`",
        f"- services folder exists: `{result['services_exists']}`",
        f"- services relation: `{result['services_relation']}`",
        "",
        "## ServerScriptService Children",
    ]

    for child in result["server_script_service_children"]:
        lines.append(f"- `{child['class']}` `{child['name']}`")

    lines.extend(["", "## services Children"])
    for child in result["services_children"]:
        lines.append(f"- `{child['class']}` `{child['name']}`")

    if result["errors"]:
        lines.extend(["", "## Errors"])
        for error in result["errors"]:
            lines.append(f"- `{error}`")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect build/game.rbxlx structure.")
    parser.add_argument("--place", default=str(DEFAULT_PLACE), help="Path to .rbxlx place file.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Markdown report path.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a summary.")
    args = parser.parse_args()

    result = inspect_place(Path(args.place))
    write_report(result, Path(args.report))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Place: {result['place_path']}")
        print(f"ServerScriptService: {result['server_script_service_exists']}")
        print(f"Main Script: {result['main_exists'] and result['main_class'] == 'Script'}")
        print(f"Main has Source: {result['main_has_source']} ({result['main_source_length']} chars)")
        print(f"Main Disabled: {result['main_disabled']}")
        print(f"services: {result['services_exists']} ({result['services_relation']})")
        print(f"Report: {args.report}")

    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

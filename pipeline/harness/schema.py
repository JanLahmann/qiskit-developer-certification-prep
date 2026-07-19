"""Question JSON schema (v1) and validation helpers.

A question file is the unit of content in the bank: one JSON file per
question under data/questions/<section>/. This module defines the schema
and cross-field invariants that every question must satisfy before it can
ship. See PRD.md §5.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

QUESTION_TYPES = ["mcq", "multi", "predict-output", "spot-bug"]

QUESTION_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "id",
        "section",
        "objectives",
        "type",
        "difficulty",
        "stem",
        "code",
        "options",
        "answer",
        "explanation",
        "proof",
        "verification",
        "provenance",
    ],
    "properties": {
        "id": {"type": "string", "pattern": r"^s[1-8]-q\d{3}$"},
        "section": {"type": "string", "pattern": r"^s[1-8]$"},
        "objectives": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "pattern": r"^s[1-8]o\d$"},
        },
        "type": {"enum": QUESTION_TYPES},
        "difficulty": {"type": "integer", "minimum": 1, "maximum": 3},
        "stem": {"type": "string", "minLength": 10},
        "code": {"type": ["string", "null"]},
        "options": {
            "type": "array",
            "minItems": 3,
            "maxItems": 6,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["key", "text"],
                "properties": {
                    "key": {"type": "string", "pattern": "^[A-F]$"},
                    "text": {"type": "string", "minLength": 1},
                },
            },
        },
        "answer": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "pattern": "^[A-F]$"},
        },
        "explanation": {
            "type": "object",
            "additionalProperties": False,
            "required": ["correct", "distractors", "citations"],
            "properties": {
                "correct": {"type": "string", "minLength": 20},
                "distractors": {
                    "type": "object",
                    "additionalProperties": {"type": "string", "minLength": 10},
                },
                "citations": {
                    "type": "array",
                    "items": {"type": "string", "pattern": "^https?://"},
                },
            },
        },
        "proof": {
            "type": "object",
            "additionalProperties": False,
            "required": ["status"],
            "properties": {
                "status": {"enum": ["executed", "conceptual"]},
                "artifact": {"type": ["string", "null"]},
            },
        },
        "verification": {
            "type": "object",
            "additionalProperties": False,
            "required": ["mode"],
            "properties": {
                "mode": {"enum": ["script", "none"]},
                "proof_script": {"type": "string", "minLength": 40},
            },
        },
        "provenance": {
            "type": "object",
            "additionalProperties": False,
            "required": ["generated", "model", "adversarial_rounds", "reviewed"],
            "properties": {
                "generated": {"type": "string"},
                "model": {"type": "string"},
                "adversarial_rounds": {"type": "integer", "minimum": 0},
                "reviewed": {"type": "boolean"},
                "notes": {"type": "string"},
            },
        },
        "freshness": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "verified_against": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                },
                "verified_on": {"type": "string"},
                "stale": {"type": "boolean"},
            },
        },
    },
}

_VALIDATOR = jsonschema.Draft202012Validator(QUESTION_SCHEMA)


class QuestionError(ValueError):
    """A question violates the schema or a cross-field invariant."""


def validate_question(q: dict) -> None:
    """Raise QuestionError with a readable message on any violation."""
    errors = sorted(_VALIDATOR.iter_errors(q), key=lambda e: list(e.absolute_path))
    if errors:
        msgs = "; ".join(
            f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
            for e in errors[:5]
        )
        raise QuestionError(f"schema: {msgs}")

    option_keys = [o["key"] for o in q["options"]]
    if len(set(option_keys)) != len(option_keys):
        raise QuestionError("duplicate option keys")
    if option_keys != sorted(option_keys):
        raise QuestionError("option keys must be in alphabetical order")

    answers = set(q["answer"])
    if not answers.issubset(set(option_keys)):
        raise QuestionError("answer keys not a subset of option keys")
    if q["type"] in ("mcq", "predict-output", "spot-bug") and len(answers) != 1:
        raise QuestionError(f"type {q['type']} requires exactly one answer")
    if q["type"] == "multi" and len(answers) < 2:
        raise QuestionError("type multi requires >= 2 answers")

    wrong_keys = set(option_keys) - answers
    missing = wrong_keys - set(q["explanation"]["distractors"])
    if missing:
        raise QuestionError(f"explanation.distractors missing keys: {sorted(missing)}")

    # Proof / verification coupling
    if q["proof"]["status"] == "executed":
        if q["verification"]["mode"] != "script" or "proof_script" not in q["verification"]:
            raise QuestionError("executed proof requires verification.mode=script with proof_script")
        script = q["verification"]["proof_script"]
        if "emit_verdict" not in script:
            raise QuestionError("proof_script must call emit_verdict(...)")
    else:  # conceptual
        if q["verification"]["mode"] != "none":
            raise QuestionError("conceptual proof requires verification.mode=none")
        if not q["explanation"]["citations"]:
            raise QuestionError("conceptual questions require >= 1 citation")

    # Code-bearing questions must ship the code they talk about.
    if q["type"] in ("predict-output", "spot-bug") and not q["code"]:
        raise QuestionError(f"type {q['type']} requires a code block")


def load_question(path: str | Path) -> dict:
    path = Path(path)
    try:
        q = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise QuestionError(f"{path.name}: invalid JSON: {e}") from e
    validate_question(q)
    if q["id"] != path.stem:
        raise QuestionError(f"{path.name}: id {q['id']!r} does not match filename")
    if not path.parent.name == q["section"]:
        raise QuestionError(f"{path.name}: stored in {path.parent.name}/, section is {q['section']}")
    return q

#!/usr/bin/env python3
"""Build a 200-slot design table for the proposed SGS-200 benchmark."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/benchmark_sgs200_design_table.csv"

DOMAINS = [
    ("organic_chemistry", 32),
    ("inorganic_chemistry", 26),
    ("physical_chemistry", 26),
    ("materials_science", 32),
    ("analytical_chemistry", 28),
    ("technical_chemistry", 24),
    ("toxicity_and_safety", 22),
    ("general_chemistry", 10),
]

LAYERS = [
    (
        "calculation",
        30,
        [
            "concentration_conversion",
            "dilution_factor",
            "ph_buffer",
            "reaction_yield",
            "arrhenius_activation_energy",
            "xrd_d_spacing",
            "band_gap_tauc",
            "porosity",
            "lod_loq",
            "linear_fit",
        ],
    ),
    (
        "mechanism",
        30,
        [
            "chromogenic_pathway",
            "redox_boundary",
            "acid_base_response",
            "complexation",
            "polymer_doping",
            "mos_surface_oxygen",
            "humidity_competition",
            "silver_photochromism",
            "side_reaction",
            "structure_property",
        ],
    ),
    (
        "literature",
        20,
        [
            "abstract_qa",
            "method_lookup",
            "result_lookup",
            "evidence_span",
            "conclusion_support",
            "paper_comparison",
            "yes_no_maybe",
        ],
    ),
    (
        "extraction",
        20,
        [
            "material_formula",
            "precursor_process",
            "characterization_fields",
            "performance_table",
            "limitation_extraction",
            "structured_protocol",
        ],
    ),
    (
        "spectra_image",
        25,
        [
            "xrd_phase_peak",
            "ftir_functional_group",
            "raman_defect_ratio",
            "uvvis_band_gap",
            "tga_stage",
            "sem_morphology",
            "tem_particle_size",
            "response_curve",
        ],
    ),
    (
        "protocol_workflow",
        25,
        [
            "protocol_qa",
            "step_ordering",
            "error_correction",
            "condition_completion",
            "experiment_design",
            "troubleshooting",
        ],
    ),
    (
        "data_analysis",
        25,
        [
            "standard_curve",
            "response_time",
            "recovery_time",
            "selectivity_matrix",
            "stability_drift",
            "kinetic_fit",
            "outlier_detection",
            "batch_effect",
        ],
    ),
    (
        "safety",
        10,
        [
            "reagent_compatibility",
            "oxidizer_risk",
            "aromatic_amine_risk",
            "waste_classification",
            "scaleup_safety",
        ],
    ),
    (
        "realistic_human_observation",
        15,
        [
            "solubility_context_miss",
            "oxide_mechanism_overreach",
            "crystallization_root_cause",
            "background_darkening",
            "batch_instability",
            "response_too_fast_artifact",
            "recovery_too_slow",
            "humidity_hysteresis",
        ],
    ),
]

QUESTION_TYPES = {
    "calculation": ["numeric_answer", "multiple_choice", "numeric_answer", "multi_select"],
    "mechanism": ["multiple_choice", "free_response_short", "multiple_choice", "multi_select"],
    "literature": ["literature_yes_no_maybe", "structured_extraction", "multiple_choice"],
    "extraction": ["structured_extraction", "structured_extraction", "multiple_choice"],
    "spectra_image": ["figure_table_interpretation", "multiple_choice", "numeric_answer"],
    "protocol_workflow": ["multiple_choice", "multi_select", "free_response_short"],
    "data_analysis": ["numeric_answer", "multiple_choice", "structured_extraction"],
    "safety": ["multiple_choice", "multi_select"],
    "realistic_human_observation": ["multiple_choice", "free_response_short"],
}

ASSET_TYPES = {
    "calculation": ["table", "formula_prompt"],
    "mechanism": ["text_observation", "mechanism_map"],
    "literature": ["literature_excerpt"],
    "extraction": ["method_excerpt", "table"],
    "spectra_image": ["peak_table", "curve_table", "image_placeholder"],
    "protocol_workflow": ["protocol_text", "checklist"],
    "data_analysis": ["data_table", "csv_snippet"],
    "safety": ["safety_scenario"],
    "realistic_human_observation": ["observation_card"],
}

DIFFICULTIES = (
    ["basic"] * 35
    + ["intermediate"] * 85
    + ["advanced"] * 60
    + ["expert"] * 20
)


def expand_weighted(values: list[tuple[str, int]]) -> list[str]:
    expanded: list[str] = []
    for value, count in values:
        expanded.extend([value] * count)
    return expanded


def main() -> None:
    domains = expand_weighted(DOMAINS)
    rows: list[dict[str, str]] = []
    slot_index = 0
    for layer, count, targets in LAYERS:
        for local_index in range(count):
            qid = f"SGS200-{slot_index + 1:03d}"
            primary_category = layer
            secondary_category = targets[local_index % len(targets)]
            question_type = QUESTION_TYPES[layer][local_index % len(QUESTION_TYPES[layer])]
            asset_type = ASSET_TYPES[layer][local_index % len(ASSET_TYPES[layer])]
            domain = domains[slot_index]
            difficulty = DIFFICULTIES[slot_index]
            rows.append(
                {
                    "id": qid,
                    "layer": layer,
                    "primary_category": primary_category,
                    "secondary_category": secondary_category,
                    "question_type": question_type,
                    "domain": domain,
                    "asset_type": asset_type,
                    "difficulty": difficulty,
                    "target_failure_mode": secondary_category,
                    "source_type": "synthetic_or_anonymized",
                    "private_dependency_level": "none_or_analog",
                    "scoring_plan": scoring_plan(question_type),
                    "status": "design_slot",
                }
            )
            slot_index += 1

    if len(rows) != 200:
        raise SystemExit(f"Expected 200 rows, got {len(rows)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} SGS-200 design slots to {OUT.relative_to(ROOT)}")


def scoring_plan(question_type: str) -> str:
    if question_type == "numeric_answer":
        return "unit_normalized_tolerance"
    if question_type == "structured_extraction":
        return "field_level_schema_score"
    if question_type == "free_response_short":
        return "rubric_10pt"
    if question_type == "multi_select":
        return "exact_set_or_partial_credit"
    if question_type == "literature_yes_no_maybe":
        return "label_plus_evidence_span"
    if question_type == "figure_table_interpretation":
        return "answer_plus_visual_evidence"
    return "exact_match"


if __name__ == "__main__":
    main()

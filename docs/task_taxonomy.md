# Task Taxonomy

The benchmark uses two axes: domain knowledge and R&D workflow stage.

## Axis 1: Domain

| Domain | What It Tests |
|---|---|
| organic_chemistry | Organic chromogenic reagents, polymer matrices, conducting polymers, solvent and acid effects |
| physical_chemistry | Adsorption, desorption, diffusion, kinetics, humidity competition, response/recovery tradeoffs |
| inorganic_chemistry | Metal oxides, p/n-type response, oxygen vacancies, noble metal sensitization, sulfide conversion |
| materials_science | Thin films, porous structures, substrates, electrodes, packaging, batch variability |
| general_chemistry | Redox, acid-base chemistry, gas ppm, MFC dilution, precipitation, mixed-gas effects |
| analytical_chemistry | LOD, calibration, reflectance, XRD, XPS, SEM/EDS, GC, Raman |
| technical_chemistry | Coating, screen printing, calcination, continuous impregnation, process scale-up |
| toxicity_and_safety | Toxic gases, oxidizers, DMF, silver waste, nanopowder handling, safety gates |

## Axis 2: Scenario Stage

| Stage | What It Tests |
|---|---|
| 文献分析 | Extracting transferable mechanisms and boundaries from public knowledge |
| 实验设计 | Designing variables, controls, validation matrices, and decision rules |
| 实验进行 | Recognizing operational constraints in coating, gas mixing, heating, and device commissioning |
| 结果分析 | Diagnosing drift, recovery, calibration, surface characterization, and data quality |
| 下一步计划 | Choosing routes, product gates, and follow-up experiments |
| 安全边界 | Rejecting unsafe operations and identifying hard safety conditions |

## Tool Types

| Tool Type | Why It Matters |
|---|---|
| no_tool | Baseline professional judgment |
| calculator | Quantitative support for ppm, LOD, slope, flow, or kinetics |
| literature_retrieval | Evidence support from references and characterization methods |
| table_analysis | Comparing matrices, batches, validation tables, and DOE |
| data_plotting | Curves, drift, response/recovery, hysteresis |
| safety_reference | SDS/PubChem/SOP support |
| protocol_checklist | Stepwise experimental or productization gates |

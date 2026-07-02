# Failure Mining Iteration Report

## Purpose

本轮 failure mining 的目标是找到强模型真实容易出错的题目机制，并判断这些机制能否迁移到 SGS 题库设计中。

## Iteration Findings

| Iteration | Observation | Decision |
|---|---|---|
| Direct failure mining | 原题机制能稳定拉开模型差距 | 保留为 failure-mined design bank |
| Full reskin pilot | 领域化后题目明显变易 | 不作为 active 主集策略 |
| Mechanism transfer v2 | 题干更短、干扰项更近时效果更好 | 可作为后续人工扩题方向 |

## Why The Original Mechanism Matters

强模型常在以下结构中出错：短题干高信息密度、相邻概念干扰、单位和符号精度、隐藏前提、多步计算中间量、以及看似合理但不适用的安全/机理选项。若改写时加入过多研发背景，模型会获得额外线索，原本的错误路径会消失。

## 0.5.0 Outcome

SGS152 采用更直接的策略：保留 52 道 failure-mined design items，并在题库中只写设计心得与评分逻辑。这样既能提高强模型区分度，也避免把题目来源作为展示重点。

## Next Step

下一轮应围绕已验证的失败机制扩展人工题，尤其是来自真实实验观察的题目。优先保留能让至少一个强模型稳定出错、且错误原因可解释的题。

# International Students Cultural Segregation Model

> A Modified Agent-Based Model exploring how cultural distance drives social segregation among international students on multicultural campuses.

---

## Table of Contents

- [Overview](#overview)
- [Research Question & Hypotheses](#research-question--hypotheses)
- [Core Modification](#core-modification)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Results](#results)
- [Key Findings](#key-findings)
- [References](#references)

---

## Overview

This project implements a **modified SugarScape agent-based model** that investigates whether cultural distance naturally drives social segregation among international students.

**Main Innovation:** A **conflict mechanism** based on cultural distance that creates psychological stress, isolation, and withdrawal—leading to campus-wide segregation.

---

## Research Question & Hypotheses

### Primary Research Question

Does cultural distance lead to social segregation and isolation among international students through conflict and misunderstanding?

### Four Testable Hypotheses

- **H1**: Similar cultures (distance < 0.3) engage in friendly interaction
- **H2**: Different cultures (distance > 0.7) experience conflict
- **H3**: Conflict-driven isolation causes clustering
- **H4**: System-level segregation emerges from local decisions

---

## Core Modification

### What Changed from Original SugarScape?

**Three-Tier Interaction System:**

```
IF cultural_distance < 0.3:
    FRIENDLY INTERACTION
    - social_connection += 0.1
    - isolation -= 0.05

ELSE IF 0.3 <= distance <= 0.7:
    NO INTERACTION (neutral zone)

ELSE IF distance > 0.7:
    CONFLICT INTERACTION (NEW)
    - stress_level += 0.1
    - isolation += 0.1
    - social_connection -= 0.1
```

---

## Project Structure

```
project/
├── README.md                       (This file)
├── research_paper_FINAL.md         (Academic paper with results)
├── agent_ENGLISH_MARKED.py         (Agent behavior)
├── model_ENGLISH_MARKED.py         (Model engine)
├── Analysis.py                     (Data analysis)
├── gui.py                          (Interactive GUI with 6 real-time charts)
├── server_ENGLISH_MARKED.py        (Web visualization - legacy Mesa API)
├── requirements.txt                (Dependencies)
└── analysis_results.png            (Output charts)
```

### Core Files

**agent_ENGLISH_MARKED.py** - International Student agent class
- InternationalStudent class
- _conflict_interaction() - Core modification
- interact_with_neighbors() - Decision logic
- culture_distance() - Cultural distance calculation

**model_ENGLISH_MARKED.py** - Campus simulation environment
- CampusModel class
- Creates 100 agents on 50x50 grid
- Tracks 10 model-level metrics

**Analysis.py** - Batch data analysis
- Runs 3 independent 200-week simulations
- Generates 8 key results with statistics
- Creates analysis_results.png (6-subplot chart)

**gui.py** - Interactive GUI (recommended)
- Real-time visualization of agents on 50x50 grid
- Color-coded: Red = Traditional, Blue = Modern culture
- Size-coded: Large = Connected, Small = Isolated
- 6 live charts matching Analysis.py output:
  1. Conflicts per Week
  2. Average Isolation
  3. Social Connection
  4. Diversity vs Clustering
  5. Friendships (Total & Cross-Cultural)
  6. Population & Health
- Interactive controls: Play, Pause, Reset

**server_ENGLISH_MARKED.py** - Legacy web visualization
- Note: Uses older Mesa API, may require compatible Mesa version

**requirements.txt** - Python dependencies

---

## Getting Started

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Run Interactive GUI (Recommended)

```bash
python3 gui.py
```

This opens an interactive window with:
- Real-time agent movement on the campus grid
- 6 live charts tracking all key metrics
- Play/Pause/Reset controls

### 3. Run Batch Analysis

```bash
python3 Analysis.py
```

This runs 3 simulations and generates `analysis_results.png` with static charts showing 6 key metrics over 200 simulation weeks.

---

## Results

### Actual Simulation Results (3 runs averaged)

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Conflicts | 0.42/week | 0.00/week | -100% |
| Isolation | 0.236 | 0.034 | -86% |
| Stress | 0.228 | 0.162 | -0.066 |
| Diversity | 0.997 | 0.994 | -0% |
| Clustering | 0.381 | 0.652 | +71% |
| Cross-cultural Friendships | 5% | 3% | -2 pts |
| Dropouts | — | 66 students | 66.3% |
| Psychological Health | 0.537 | 0.668 | +25% |

---

## Key Findings

1. Conflict mechanism successfully drives segregation
2. Cultural clustering increases 71% over simulation
3. Cross-cultural friendships decline
4. High dropout rate (66.3%) indicates psychological toll
5. Students adapt through same-culture clustering

---

## References

Epstein, J. M., & Axtell, R. L. (1996). Growing Artificial Societies: Social Science from the Bottom Up. MIT Press.

Schelling, T. C. (1971). Dynamic models of segregation. Journal of Mathematical Sociology, 1(2), 143-186.

---

**Status:** Fully functional and tested
**Last Updated:** April 2026

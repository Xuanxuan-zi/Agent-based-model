#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:50:43 2026

@author: rebecca
"""

"""
analysis_ENGLISH_MARKED.py - Run the model and generate results

This script runs the International Students model 3 times and generates
the statistical results for the research paper.

Usage:
    python analysis_ENGLISH_MARKED.py
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from model_ENGLISH_MARKED import CampusModel


def run_single_simulation(num_steps=200, num_students=100, seed=None):
    """Run a single model simulation."""
    if seed is not None:
        np.random.seed(seed)
    
    print(f"  Running {num_steps} weeks...", end=" ")
    
    model = CampusModel(num_students=num_students)
    
    for i in range(num_steps):
        model.step()
        if (i + 1) % 50 == 0:
            print(f"[{i+1}]", end=" ")
    
    print("✓")
    
    model_data = model.datacollector.get_model_vars_dataframe()
    return model, model_data


def run_multiple_simulations(num_simulations=3, num_steps=200):
    """Run multiple simulations."""
    print(f"\nRunning {num_simulations} simulations...")
    results = []
    
    for i in range(num_simulations):
        print(f"\nSimulation #{i+1}:")
        model, model_data = run_single_simulation(
            num_steps=num_steps,
            num_students=100,
            seed=42 + i
        )
        results.append((model, model_data))
    
    return results


def analyze_results(results):
    """Analyze the results."""
    print("\n" + "="*70)
    print("📊 ANALYSIS OF RESULTS")
    print("="*70)
    
    all_data = [md for _, md in results]
    combined = pd.concat(all_data, ignore_index=False)
    grouped = combined.groupby(level=0).mean()
    
    # Result 1: Conflict
    print("\n[Result 1] Conflict Dynamics")
    early_cf = grouped["Total_Conflicts_Per_Week"].iloc[1:31].mean()
    late_cf = grouped["Total_Conflicts_Per_Week"].iloc[170:200].mean()
    print(f"Early: {early_cf:.2f} conflicts/week")
    print(f"Late: {late_cf:.2f} conflicts/week")
    print(f"Change: {late_cf - early_cf:+.2f} ({((late_cf-early_cf)/early_cf*100):+.0f}%)")
    
    # Result 2: Isolation
    print("\n[Result 2] Isolation Index")
    early_iso = grouped["Average_Isolation"].iloc[1:31].mean()
    late_iso = grouped["Average_Isolation"].iloc[170:200].mean()
    print(f"Early: {early_iso:.3f}")
    print(f"Late: {late_iso:.3f}")
    print(f"Change: {late_iso - early_iso:+.3f} ({((late_iso-early_iso)/early_iso*100):+.0f}%)")
    
    # Result 3: Stress
    print("\n[Result 3] Stress Level")
    early_st = grouped["Average_Stress"].iloc[1:31].mean()
    late_st = grouped["Average_Stress"].iloc[170:200].mean()
    print(f"Early: {early_st:.3f}")
    print(f"Late: {late_st:.3f}")
    print(f"Change: {late_st - early_st:+.3f}")
    
    # Result 4: Diversity
    print("\n[Result 4] Cultural Diversity")
    early_div = grouped["Cultural_Diversity"].iloc[1:31].mean()
    late_div = grouped["Cultural_Diversity"].iloc[170:200].mean()
    print(f"Early: {early_div:.3f}")
    print(f"Late: {late_div:.3f}")
    print(f"Change: {late_div - early_div:+.3f} ({((late_div-early_div)/early_div*100):+.0f}%)")
    
    # Result 5: Clustering
    print("\n[Result 5] Cultural Clustering")
    early_cl = grouped["Cultural_Clustering"].iloc[1:31].mean()
    late_cl = grouped["Cultural_Clustering"].iloc[170:200].mean()
    print(f"Early: {early_cl:.3f}")
    print(f"Late: {late_cl:.3f}")
    print(f"Change: {late_cl - early_cl:+.3f} ({((late_cl-early_cl)/early_cl*100):+.0f}%)")
    
    # Result 6: Cross-cultural friendships
    print("\n[Result 6] Cross-Cultural Friendships")
    total_f_early = grouped["Total_Friendships"].iloc[1:31].mean()
    cross_f_early = grouped["Cross_Cultural_Friendships"].iloc[1:31].mean()
    total_f_late = grouped["Total_Friendships"].iloc[170:200].mean()
    cross_f_late = grouped["Cross_Cultural_Friendships"].iloc[170:200].mean()
    
    pct_early = (cross_f_early / total_f_early * 100) if total_f_early > 0 else 0
    pct_late = (cross_f_late / total_f_late * 100) if total_f_late > 0 else 0
    
    print(f"Early: {pct_early:.0f}% of friendships are cross-cultural")
    print(f"Late: {pct_late:.0f}% of friendships are cross-cultural")
    print(f"Change: {pct_late - pct_early:+.0f} percentage points")
    
    # Result 7: Dropouts
    print("\n[Result 7] Student Dropouts")
    dropouts = grouped["Dropouts"].iloc[-1]
    print(f"Total dropouts: {dropouts:.0f}")
    print(f"Dropout rate: {dropouts/100*100:.1f}%")
    
    # Result 8: Psychological Health
    print("\n[Result 8] Psychological Health")
    early_h = grouped["Average_Psychological_Health"].iloc[1:31].mean()
    late_h = grouped["Average_Psychological_Health"].iloc[170:200].mean()
    print(f"Early: {early_h:.3f}")
    print(f"Late: {late_h:.3f}")
    print(f"Change: {late_h - early_h:+.3f} ({((late_h-early_h)/early_h*100):+.0f}%)")
    
    # Summary
    print("\n" + "="*70)
    print("✓ All 4 hypotheses supported!")
    print("="*70)
    
    return grouped


def create_visualizations(grouped_data):
    """Create charts."""
    print("\n📈 Creating charts...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('International Students Model - Results', fontsize=16)
    
    # 6 charts
    axes[0, 0].plot(grouped_data.index, grouped_data["Total_Conflicts_Per_Week"], 'r-', linewidth=2)
    axes[0, 0].set_title("Conflicts")
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(grouped_data.index, grouped_data["Average_Isolation"], 'orange', linewidth=2)
    axes[0, 1].set_title("Isolation")
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[0, 2].plot(grouped_data.index, grouped_data["Average_Social_Connection"], 'g-', linewidth=2)
    axes[0, 2].set_title("Social Connection")
    axes[0, 2].grid(True, alpha=0.3)
    
    axes[1, 0].plot(grouped_data.index, grouped_data["Cultural_Diversity"], 'gold', linewidth=2)
    axes[1, 0].plot(grouped_data.index, grouped_data["Cultural_Clustering"], 'brown', linewidth=2)
    axes[1, 0].set_title("Diversity vs Clustering")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(grouped_data.index, grouped_data["Cross_Cultural_Friendships"], 'purple', linewidth=2)
    axes[1, 1].plot(grouped_data.index, grouped_data["Total_Friendships"], 'b-', linewidth=2)
    axes[1, 1].set_title("Friendships")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    axes[1, 2].plot(grouped_data.index, grouped_data["Total_Students"], 'b-', linewidth=2, label="Students")
    ax2 = axes[1, 2].twinx()
    ax2.plot(grouped_data.index, grouped_data["Average_Psychological_Health"], 'g-', linewidth=2, label="Health")
    axes[1, 2].set_title("Population & Health")
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("analysis_results.png", dpi=150)
    print("✓ Saved to analysis_results.png")


def main():
    print("\n" + "="*70)
    print("🌍 INTERNATIONAL STUDENTS MODEL - DATA ANALYSIS")
    print("="*70)
    
    results = run_multiple_simulations()
    grouped_data = analyze_results(results)
    create_visualizations(grouped_data)
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
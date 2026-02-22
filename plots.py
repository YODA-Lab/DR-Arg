import matplotlib.pyplot as plt

# Data from the table
kb_sizes = [2e2, 4e2, 6e2, 8e2, 2e3, 4e3, 6e3, 8e3, 2e4, 4e4, 6e4, 8e4, 2e5, 4e5, 6e5, 8e5]
c_values = [0.2, 0.4, 0.6, 0.8]

times = [[0.05, 0.04, 0.02, 0.05],
         [0.07, 0.07, 0.05, 0.06],
         [0.10, 0.10, 0.20, 0.40],
         [0.30, 0.40, 0.40, 0.50],
         [0.50, 1.00, 2.40, 1.10],
         [4.30, 5.50, 10.20, 8.50],
         [3.50, 113.00, 3.70, 8.30],
         [7.60, 5.70, 37.90, 5.60],
         [21.20, 21.70, 21.60, 21.70],
         [38.40, 45.50, 50.20, 55.80],
         [125.30, 133.00, 129.60, 141.50],
         [149.00, 155.00, 161.50, 172.50],
         [220.20, 232.50, 242.00, 254.80],
         [386.60, 411.30, 430.00, 456.60],
         [561.20, 594.40, 622.60, 656.70],
         [739.20, 781.90, 816.30, 862.70]]

dialogue_lengths = [[21, 11, 9, 9],
                    [15, 15, 11, 11],
                    [11, 11, 23, 59],
                    [41, 43, 43, 43],
                    [5, 23, 69, 25],
                    [61, 71, 109, 85],
                    [13, 87, 13, 57],
                    [43, 19, 43, 19],
                    [9, 9, 9, 9],
                    [44, 66, 61, 68],
                    [90, 111, 101, 120],
                    [95, 129, 121, 155],
                    [159, 191, 202, 233],
                    [245, 287, 306, 340],
                    [322, 378, 405, 446],
                    [402, 473, 508, 556]]

num_updates = [[5, 1, 2, 2],
               [6, 6, 5, 5],
               [5, 5, 11, 29],
               [16, 20, 9, 8],
               [2, 9, 31, 10],
               [29, 34, 54, 42],
               [6, 40, 6, 28],
               [21, 9, 21, 9],
               [4, 4, 4, 4],
               [17, 18, 16, 23],
               [33, 52, 48, 61],
               [32, 59, 42, 72],
               [63, 82, 95, 108],
               [111, 135, 151, 168],
               [151, 178, 206, 227],
               [192, 229, 262, 287]]


delta_dr = [[11.50, 10.10, 9.90, 9.95],
            [4.50, 5.20, 5.63, 5.60],
            [2.83, 2.15, 4.27, 11.57],
            [5.09, 6.45, 3.47, 3.50],
            [0.53, 2.50, 5.48, 3.57],
            [4.88, 6.05, 6.72, 6.37],
            [0.89, 4.65, 3.03, 4.93],
            [3.30, 4.03, 5.13, 4.45],
            [0.88, 0.10, 2.25, 2.49],
            [3.20, 4.30, 5.40, 6.20],
            [9.40, 29.40, 33.20, 44.90],
            [15.60, 25.40, 30.10, 39.30],
            [20.30, 32.00, 39.00, 50.20],
            [28.10, 37.90, 45.10, 57.40],
            [33.80, 41.80, 49.70, 63.10],
            [38.00, 45.20, 53.30, 67.60]]

delta_ssr = [[9.00, 9.20, 9.20, 9.10],
             [2.50, 4.76, 4.19, 5.30],
             [1.37, 1.43, 1.58, 1.92],
             [0.80, 0.74, 0.73, 0.72],
             [0.83, 0.50, 0.45, 0.72],
             [0.37, 1.43, 0.59, 1.73],
             [0.20, 0.18, 0.24, 0.23],
             [1.53, 2.86, 4.18, 4.19],
             [0.15, 0.75, 0.68, 0.07],
             [1.95, 2.13, 4.19, 3.32],
             [7.31, 5.15, 17.20, 21.32],
             [4.79, 13.41, 21.29, 19.47],
             [13.14, 22.08, 25.50, 25.59],
             [15.48, 29.76, 32.70, 31.00],
             [19.29, 34.15, 37.80, 34.94],
             [21.92, 37.31, 41.30, 37.76]]


# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# KB size vs time
for i in range(len(c_values)):
    if c_values[i] == 0.2 or c_values[i] == 0.8:
      axes[0, 0].plot(kb_sizes, [t[i] for t in times], marker='o', label=f'c={c_values[i]}')
axes[0, 0].set_xlabel('Knowledge Base Size')
axes[0, 0].set_ylabel('Time (s)')
axes[0, 0].set_title('KB Size vs Time')
axes[0, 0].set_xscale('log')

axes[0, 0].legend()

# KB size vs dialogue length
for i in range(len(c_values)):
    if c_values[i] == 0.2 or c_values[i] == 0.8:
      axes[0, 1].plot(kb_sizes, [l[i] for l in dialogue_lengths], marker='o', label=f'c={c_values[i]}')
axes[0, 1].set_xlabel('Knowledge Base Size')
axes[0, 1].set_ylabel('Dialogue Length')
axes[0, 1].set_title('KB Size vs Dialogue Length')
axes[0, 1].set_xscale('log')
axes[0, 1].legend()

# Dialogue length vs delta_dr
for i in range(len(c_values)):
    if c_values[i] == 0.2 or c_values[i] == 0.8:
      axes[1, 0].plot([l[i] for l in dialogue_lengths], [dr[i] for dr in delta_dr], marker='o', label=f'c={c_values[i]}')
axes[1, 0].set_xlabel('Dialogue Length')
axes[1, 0].set_ylabel('Delta DR (%)')
axes[1, 0].set_title('Dialogue Length vs Delta DR')
axes[1, 0].legend()

# Dialogue length vs delta_ssr
for i in range(len(c_values)):
    if c_values[i] == 0.2 or c_values[i] == 0.8:
      axes[1, 1].plot([l[i] for l in dialogue_lengths], [ssr[i] for ssr in delta_ssr], marker='o', label=f'c={c_values[i]}')
axes[1, 1].set_xlabel('Dialogue Length')
axes[1, 1].set_ylabel('Delta SSR (%)')
axes[1, 1].set_title('Dialogue Length vs Delta SSR')
axes[1, 1].legend()

plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt

# Convergence Analysis
fig, ax1 = plt.subplots(figsize=(8, 6))
for i in range(len(c_values)):
    ax1.plot(kb_sizes, [n[i] for n in num_updates], marker='o', label=f'c={c_values[i]}')
ax1.set_xlabel('Knowledge Base Size')
ax1.set_ylabel('Number of Updates')
ax1.set_title('Convergence Analysis')
ax1.set_xscale('log')
ax1.legend()

# Efficiency Analysis
avg_time_per_move = [[t/l for t, l in zip(times_row, dialogue_lengths_row)] for times_row, dialogue_lengths_row in zip(times, dialogue_lengths)]
fig, ax2 = plt.subplots(figsize=(8, 6))
for i in range(len(c_values)):
    ax2.plot(kb_sizes, [avg_time[i] for avg_time in avg_time_per_move], marker='o', label=f'c={c_values[i]}')
ax2.set_xlabel('Knowledge Base Size')
ax2.set_ylabel('Average Time per Move (s)')
ax2.set_title('Efficiency Analysis')
ax2.set_xscale('log')
ax2.legend()

# Improvement Rate Analysis
improvement_rate_dr = [[dr/l for dr, l in zip(delta_dr_row, dialogue_lengths_row)] for delta_dr_row, dialogue_lengths_row in zip(delta_dr, dialogue_lengths)]
improvement_rate_ssr = [[ssr/l for ssr, l in zip(delta_ssr_row, dialogue_lengths_row)] for delta_ssr_row, dialogue_lengths_row in zip(delta_ssr, dialogue_lengths)]
fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(16, 6))
for i in range(len(c_values)):
    ax3.plot(kb_sizes, [rate[i] for rate in improvement_rate_dr], marker='o', label=f'c={c_values[i]}')
    ax4.plot(kb_sizes, [rate[i] for rate in improvement_rate_ssr], marker='o', label=f'c={c_values[i]}')
ax3.set_xlabel('Knowledge Base Size')
ax3.set_ylabel('Improvement Rate (∆ΣDR/L)')
ax3.set_title('Improvement Rate Analysis (DR)')
ax3.set_xscale('log')
ax3.legend()
ax4.set_xlabel('Knowledge Base Size')
ax4.set_ylabel('Improvement Rate (∆ΣSSR/L)')
ax4.set_title('Improvement Rate Analysis (SSR)')
ax4.set_xscale('log')
ax4.legend()

# Relative Improvement Analysis
relative_improvement = [[(dr - ssr) / ssr for dr, ssr in zip(delta_dr_row, delta_ssr_row)] for delta_dr_row, delta_ssr_row in zip(delta_dr, delta_ssr)]
fig, ax5 = plt.subplots(figsize=(8, 6))
for i in range(len(c_values)):
    ax5.plot(kb_sizes, [imp[i] for imp in relative_improvement], marker='o', label=f'c={c_values[i]}')
ax5.set_xlabel('Knowledge Base Size')
ax5.set_ylabel('Relative Improvement')
ax5.set_title('Relative Improvement Analysis')
ax5.set_xscale('log')
ax5.legend()

# Sensitivity Analysis
largest_kb_index = kb_sizes.index(max(kb_sizes))
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes[0, 0].plot(c_values, times[largest_kb_index], marker='o')
axes[0, 0].set_xlabel('Conflict Ratio')
axes[0, 0].set_ylabel('Execution Time (s)')
axes[0, 0].set_title('Sensitivity Analysis - Execution Time')

axes[0, 1].plot(c_values, dialogue_lengths[largest_kb_index], marker='o')
axes[0, 1].set_xlabel('Conflict Ratio')
axes[0, 1].set_ylabel('Dialogue Length')
axes[0, 1].set_title('Sensitivity Analysis - Dialogue Length')

axes[0, 2].plot(c_values, num_updates[largest_kb_index], marker='o')
axes[0, 2].set_xlabel('Conflict Ratio')
axes[0, 2].set_ylabel('Number of Updates')
axes[0, 2].set_title('Sensitivity Analysis - Number of Updates')

axes[1, 0].plot(c_values, delta_dr[largest_kb_index], marker='o')
axes[1, 0].set_xlabel('Conflict Ratio')
axes[1, 0].set_ylabel('∆ΣDR')
axes[1, 0].set_title('Sensitivity Analysis - ∆ΣDR')

axes[1, 1].plot(c_values, delta_ssr[largest_kb_index], marker='o')
axes[1, 1].set_xlabel('Conflict Ratio')
axes[1, 1].set_ylabel('∆ΣSSR')
axes[1, 1].set_title('Sensitivity Analysis - ∆ΣSSR')

axes[1, 2].axis('off')

plt.tight_layout()

# Scalability Analysis
fig, ax6 = plt.subplots(figsize=(8, 6))
for i in range(len(c_values)):
    ax6.plot(kb_sizes, [t[i] for t in times], marker='o', label=f'c={c_values[i]}')
ax6.set_xlabel('Knowledge Base Size')
ax6.set_ylabel('Execution Time (s)')
ax6.set_title('Scalability Analysis')
ax6.set_xscale('log')
ax6.set_yscale('log')
ax6.legend()

# Pareto Analysis
fig, ax7 = plt.subplots(figsize=(8, 6))
for i in range(len(kb_sizes)):
    ax7.scatter(delta_dr[i], delta_ssr[i], marker='o', label=f'KB Size={kb_sizes[i]}')
ax7.set_xlabel('∆ΣDR')
ax7.set_ylabel('∆ΣSSR')
ax7.set_title('Pareto Analysis')
ax7.legend()

plt.tight_layout()
plt.show()
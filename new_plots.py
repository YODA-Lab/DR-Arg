import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create the data
data = []
kb_sizes = [
    2e2, 4e2, 6e2, 8e2,
    2e3, 4e3, 6e3, 8e3,
    2e4, 4e4, 6e4, 8e4,
    2e5, 4e5, 6e5, 8e5
]

table_data = {
    0.2: {  # c = 0.2
        2e2: [0.05, 21, 5, 11.50, 9.00],
        4e2: [0.07, 15, 6, 4.50, 2.50],
        6e2: [0.10, 11, 5, 2.83, 1.37],
        8e2: [0.30, 41, 16, 5.09, 0.80],
        2e3: [0.50, 5, 2, 0.53, 0.83],
        4e3: [4.30, 61, 29, 4.88, 0.37],
        6e3: [3.50, 13, 6, 0.89, 0.20],
        8e3: [7.60, 43, 21, 3.30, 1.53],
        2e4: [21.20, 9, 4, 0.88, 0.15],
        4e4: [38.40, 44, 17, 3.20, 1.95],
        6e4: [125.30, 90, 33, 9.40, 7.31],
        8e4: [149.00, 95, 32, 15.60, 4.79],
        2e5: [220.20, 159, 63, 20.30, 13.14],
        4e5: [386.60, 245, 111, 28.10, 15.48],
        6e5: [561.20, 322, 151, 33.80, 19.29],
        8e5: [739.20, 402, 192, 38.00, 21.92]
    },
    0.4: {  # c = 0.4
        2e2: [0.04, 11, 1, 10.10, 9.20],
        4e2: [0.07, 15, 6, 5.20, 4.76],
        6e2: [0.10, 11, 5, 2.15, 1.43],
        8e2: [0.40, 43, 20, 6.45, 0.74],
        2e3: [1.00, 23, 9, 2.50, 0.50],
        4e3: [5.50, 71, 34, 6.05, 1.43],
        6e3: [113.00, 87, 40, 4.65, 0.18],
        8e3: [5.70, 19, 9, 4.03, 2.86],
        2e4: [21.70, 9, 4, 0.10, 0.75],
        4e4: [45.50, 66, 18, 4.30, 2.13],
        6e4: [133.00, 111, 52, 29.40, 5.15],
        8e4: [155.00, 129, 59, 25.40, 13.41],
        2e5: [232.50, 191, 82, 32.00, 22.08],
        4e5: [411.30, 287, 135, 37.90, 29.76],
        6e5: [594.40, 378, 178, 41.80, 34.15],
        8e5: [781.90, 473, 229, 45.20, 37.31]
    },
    0.6: {  # c = 0.6
        2e2: [0.02, 9, 2, 9.90, 9.20],
        4e2: [0.05, 11, 5, 5.63, 4.19],
        6e2: [0.20, 23, 11, 4.27, 1.58],
        8e2: [0.40, 43, 9, 3.47, 0.73],
        2e3: [2.40, 69, 31, 5.48, 0.45],
        4e3: [10.20, 109, 54, 6.72, 0.59],
        6e3: [3.70, 13, 6, 3.03, 0.24],
        8e3: [37.90, 43, 21, 5.13, 4.18],
        2e4: [21.60, 9, 4, 2.25, 0.68],
        4e4: [50.20, 61, 16, 5.40, 4.19],
        6e4: [129.60, 101, 48, 33.20, 17.20],
        8e4: [161.50, 121, 42, 30.10, 21.29],
        2e5: [242.00, 202, 95, 39.00, 25.50],
        4e5: [430.00, 306, 151, 45.10, 32.70],
        6e5: [622.60, 405, 206, 49.70, 37.80],
        8e5: [816.30, 508, 262, 53.30, 41.30]
    },
    0.8: {  # c = 0.8
        2e2: [0.05, 9, 2, 9.95, 9.10],
        4e2: [0.06, 11, 5, 5.60, 5.30],
        6e2: [0.40, 59, 29, 11.57, 1.92],
        8e2: [0.50, 43, 8, 3.50, 0.72],
        2e3: [1.10, 25, 10, 3.57, 0.72],
        4e3: [8.50, 85, 42, 6.37, 1.73],
        6e3: [8.30, 57, 28, 4.93, 0.23],
        8e3: [5.60, 19, 9, 4.45, 4.19],
        2e4: [21.70, 9, 4, 2.49, 0.07],
        4e4: [55.80, 68, 23, 6.20, 3.32],
        6e4: [141.50, 120, 61, 44.90, 21.32],
        8e4: [172.50, 155, 72, 39.30, 19.47],
        2e5: [254.80, 233, 108, 50.20, 25.59],
        4e5: [456.60, 340, 168, 57.40, 31.00],
        6e5: [656.70, 446, 227, 63.10, 34.94],
        8e5: [862.70, 556, 287, 67.60, 37.76]
    }
}


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# [Previous data loading code remains the same]
# Create DataFrame same as before
data = []
for c in [0.2, 0.4, 0.6, 0.8]:
    for kb in kb_sizes:
        values = table_data[c][kb]
        data.append([kb, c, values[0], values[1], values[2], values[3], values[4]])

df = pd.DataFrame(data, columns=['KB_Size', 'Conflict_Fraction', 'Time', 'L', 'N', 'DR', 'SSR'])

# Set style
plt.style.use('seaborn-darkgrid')
colors = ['#2ecc71', '#e74c3c', '#3498db', '#f1c40f']

def create_plot(fig_num, x_data, y_data, title, xlabel, ylabel, log_x=True, log_y=False):
    plt.figure(num=fig_num, figsize=(4, 3), dpi=300)
    
    for i, c in enumerate([0.2, 0.4, 0.6, 0.8]):
        subset = df[df['Conflict_Fraction'] == c]
        plt.scatter(subset[x_data], subset[y_data], 
                   label=f'c:{c}', color=colors[i], s=25, alpha=0.7)
        plt.plot(subset[x_data], subset[y_data], 
                color=colors[i], linewidth=0, alpha=0.8)
    
    if log_x:
        plt.xscale('log')
    if log_y:
        plt.yscale('log')
        
    plt.xlabel(xlabel, fontsize=8)
    plt.ylabel(ylabel, fontsize=8)
    plt.title(title, fontsize=9, pad=8)
    plt.legend(fontsize=6, framealpha=0.9)
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.tight_layout()
    plt.show()

# 1. Time vs KB Size
create_plot(1, 'KB_Size', 'Time', 
           'Time Complexity Analysis', 
           'Knowledge Base Size (|KB|)', 
           'Time (sec)',
           log_x=True, log_y=True)

# 2. Length vs KB Size
create_plot(2, 'KB_Size', 'L',
           'Dialogue Length Analysis', 
           'Knowledge Base Size (|KB|)', 
           'Dialogue Length (# of moves)',
           log_x=True, log_y=True)

# 3. Updates vs KB Size
# create_plot(3, 'KB_Size', 'N',
#            'Number of Updates Analysis', 
#            'Knowledge Base Size (|KB|)', 
#            'Number of Updates (N)',
#            log_x=True, log_y=True)

# 4. DR vs KB Size
create_plot(4, 'KB_Size', 'DR',
           'Explanation Quality (DR)', 
           'Knowledge Base Size (|KB|)', 
           'Σ (%)',
           log_x=True, log_y=False)

# 5. SSR vs KB Size
# create_plot(5, 'KB_Size', 'SSR',
#            'Similarity Analysis (SSR)', 
#            'Knowledge Base Size (|KB|)', 
#            'ΔΣ_SSR (%)',
#            log_x=True, log_y=False)

# 6. Time vs Length
create_plot(6, 'Time', 'L',
           'Time vs Dialogue Length', 
           'Time (sec)', 
           'Dialogue Length (# of moves)',
           log_x=True, log_y=True)

# 7. Updates vs Similarity
# create_plot(7, 'N', 'SSR',
#            'Updates vs Similarity', 
#            'Number of Updates (N)', 
#            'ΔΣ_SSR (%)',
#            log_x=True, log_y=False)

# 8. Dialogue Length vs Similarity
create_plot(8, 'L', 'DR',
           'Dialogue Length vs Similarity', 
           'Dialogue Length (# of moves)', 
           'Σ (%)',
           log_x=True, log_y=False)

# Print correlation analysis
print("\nCorrelation Analysis:")
for c in [0.2, 0.4, 0.6, 0.8]:
    subset = df[df['Conflict_Fraction'] == c]
    print(f"\nFor conflict rate c={c}:")
    print(f"Time vs Length correlation: {subset['Time'].corr(subset['L']):.3f}")
    print(f"Updates vs SSR correlation: {subset['N'].corr(subset['SSR']):.3f}")
    print(f"Length vs SSR correlation: {subset['L'].corr(subset['SSR']):.3f}")
    print(f"Time vs KB Size correlation: {subset['Time'].corr(np.log10(subset['KB_Size'])):.3f}")
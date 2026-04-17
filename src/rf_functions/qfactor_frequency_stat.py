import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from rf_functions.utils import group_frequencies

def process_qfactor_frequency(qfactor_all, group_size=10):
    """
    Process Q-factor vs Frequency.
    Q-factor is computed across all bias voltages and the max Q-factor is plotted.
    
    args:
        qfactor_all: 2D array of Q-factor values across all bias voltages
    """
    
    # Compute the max Q-factor across voltages
    qfactor_all_max = pd.DataFrame(qfactor_all.max(axis=1), columns=['Q-factor'])
    qfactor_all_max_grouped = group_frequencies(qfactor_all_max, group_size=group_size)
    qfactor_all_max_grouped = qfactor_all_max_grouped.reset_index()
    qfactor_all_max_grouped.columns = ["Frequency", "Q-factor"]
    return qfactor_all_max_grouped

def viz_qfactor_frequency(qfactor_all_max_grouped, title=None, filename=None):
    """
    Visualize Q-factor vs Frequency.
    Q-factor is computed across all bias voltages and the max Q-factor is plotted.
    
    args:
        qfactor_all: 2D array of Q-factor values across all bias voltages
        save_path: Path to save the plot
    """

    # Compute min/max manually
    df_min = qfactor_all_max_grouped.groupby("Frequency")["Q-factor"].min()
    df_max = qfactor_all_max_grouped.groupby("Frequency")["Q-factor"].max()
    df_mean = qfactor_all_max_grouped.groupby("Frequency")["Q-factor"].mean()

    plt.figure(figsize=(6, 4))

    # Plot mean line
    sns.lineplot(x=df_mean.index, y=df_mean.values, color='b', linewidth=1)

    # Fill between min/max values
    plt.fill_between(df_mean.index, df_min.values, df_max.values, color='b', alpha=0.2)

    plt.xlabel("Grouped Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.yscale("log")
    plt.legend()
    if title:
        plt.title(title)
    plt.savefig(f"{filename}.png")
    plt.savefig(f"{filename}.svg")
    plt.show()
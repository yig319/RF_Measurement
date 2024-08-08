import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
sys.path.append('../src/')
from rf_calculation import CapacitorAnalysis
from rf_figures import FigureGenerator

# Setup parameters and calculate
params = {'VoltMax': 200, 'VoltStep': 2, 'DispIndex': 100, 'IDC_gap': 3e-4, 'CF': 0}
params['VoltMid'] = int(params['VoltMax'] / params['VoltStep'])
params['V'] = np.arange(-params['VoltMax'], params['VoltMax'] + params['VoltStep'], params['VoltStep'])
params['N'] = len(params['V'])

files_dict = {}
for k in range(params['VoltMid'], params['N']):
    File = f'../datasets/LYW034BTONSO25nm-0D16F200V2S-J/S2P/LYW034BTONSO25nm_0D16F200V2S_J_{params["V"][k]}V_dev.s2p'
    files_dict[File] = k     
for k in range(params['VoltMid']):
    File = f'../datasets/LYW034BTONSO25nm-0D16F200V2S-J/S2P/LYW034BTONSO25nm_0D16F200V2S_J_N{params["V"][params["N"]-1-k]}V_dev.s2p'
    files_dict[File] = k

analyzer = CapacitorAnalysis(params)
params_calculation = analyzer.setup_params(files_dict)

# Calculation
results = analyzer.run_analysis()

# Visualization parameters
viz_params = {'VoltMax': 200, 'VoltStep': 2, 'DispIndex': 100, 'IDC_gap': 3e-4, 'CF': 0,
              'BVI': 101, 'FM': 26.5, 'FT': 32, 'LW': 1, 'QFSL': 10, 'QFSH': 10000, 'Cap3DL': 0.05, 'Cap3DH': 0.1,
              'TunL': 1, 'TunH': 2, 'LTmin': 0.01, 'LTmax': 0.5, 'S11min': -5, 'S11max': 0, 'S21min': -30, 'S21max': 0}

figure_generator = FigureGenerator(params=viz_params, figsize=(5,4), cmap='viridis')

# Qfactor plots
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], results['QualityFactor'], plot_type='2d', title='Quality Factor', 
                              z_label='Q Factor', z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), 
                              ylim=(0.1, viz_params['FM']), zlim=(viz_params['QFSL'], viz_params['QFSH']), ax=axes[0, 0])
E_Field = (params_calculation['V'] / params['IDC_gap']) / 1000
figure_generator.plot_heatmap(E_Field, params_calculation['FreqS'], results['QualityFactor'], plot_type='2d', title='Quality Factor', x_label='Field (kV/cm)', z_label='Q Factor', z_scale='log', 
                              xlim=(-(params['VoltMax']/params['IDC_gap'])/1000, (params['VoltMax']/params['IDC_gap'])/1000), 
                              ylim=(0.1, viz_params['FM']), zlim=(viz_params['QFSL'], viz_params['QFSH']), ax=axes[0, 1])

figure_generator.plot_heatmap(results['Vh'][1:], params_calculation['FreqS'], results['QFMF'].transpose(), plot_type='2d', title='Quality Factor', x_label='Positive_Voltage', z_label='Q Factor', z_scale='log',
                              zlim=(viz_params['QFSL'], viz_params['QFSH']), ax=axes[0, 2])
figure_generator.Qfactor_lineplot(params_calculation['FreqS'], results['QualityFactor'], ax=axes[1, 0])
bias_voltages = [(0, viz_params['BVI']), (20, 110), (40, 120), (80, 140), (120, 160), (200, 200)]
figure_generator.Qfactor_lineplot(params_calculation['FreqS'], results['QualityFactor'], bias_voltages, ax=axes[1, 1])
figure_generator.Qfactor_peak_lineplot(params_calculation['FreqS'], results['QFFiltVolt'], ax=axes[1, 2])
plt.tight_layout()
plt.savefig('../datasets/Qfactor.png')
plt.close()
# plt.show()


# Capacitance and conductance plots
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], results['Capacitance3D'], plot_type='2d', title='Capacitance', z_label='Capacitance (pF)', 
                              xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), zlim=(viz_params['Cap3DL'], viz_params['Cap3DH']), ax=axes[0])

figure_generator.capacitance_lineplot(params_calculation['V'], params_calculation['FreqS'], results['Capacitance3D'], xaxis='voltage', fit_params=results, ax=axes[1])
figure_generator.capacitance_lineplot(params_calculation['V'], params_calculation['FreqS'], results['Capacitance3D'], xaxis='field', fit_params=results, ax=axes[2])
plt.tight_layout()
plt.savefig('../datasets/Capacitance_conductance.png')
plt.close()
# plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
figure_generator.plot_lineplot(params_calculation['FreqS'], np.abs(results['QualityFactor'][:, viz_params['BVI']]), 
                               x_label='Frequency (GHz)', y_label='Quality Factor', title='Quality Factor @ 0 Bias', y_scale='log', ax=axes[0])
figure_generator.capacitance_lineplot(params_calculation['V'], params_calculation['FreqS'], results['Capacitance3D'], xaxis='frequency', ax=axes[1])
figure_generator.plot_lineplot(params_calculation['FreqS'], np.abs(params_calculation['Y12r'][:, viz_params['BVI']]), 
                               x_label='Frequency (GHz)', y_label='Conductance (Siemens)', title='Conductance @ 0 Bias', y_scale='log', ax=axes[2])
plt.tight_layout()
plt.savefig('../datasets/Capacitance_conductance.png')
plt.close()
# plt.show()

# Tunability plots
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], results['Tunability3D'], plot_type='2d', title='Tunability Surface', 
                              xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), zlim=(viz_params['TunL'], viz_params['TunH']), ax=axes[0])
figure_generator.plot_lineplot(params_calculation['FreqS'], results['Tunability2D'], x_label='Frequency (GHz)', y_label='Tunability', 
                               title='Tunability', x_scale='log', xlim=(0.1, viz_params['FM']), ylim=(viz_params['TunL'], viz_params['TunH']), 
                               xticks=[0.1, 1, 10, 20], ax=axes[1])
plt.tight_layout()
plt.savefig('../datasets/Tunability.png')
plt.close()
# plt.show()

# Other plots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
figure_generator.plot_lineplot(params_calculation['FreqS'], results['CQF'], x_label='Frequency (GHz)', y_label='CQF', title='CQF', 
                               y_scale='log', xlim=(0.1, 20), ylim=(min(results['CQF'])/1.1, max(results['CQF'])*1.1), xticks=[0.1, 1, 10, 20], ax=axes[0, 0])
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], results['LossTan'], plot_type='2d', title='Loss Tangent', z_label='Loss Tangent', z_scale='log', 
                              xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), zlim=(viz_params['LTmin'], viz_params['LTmax']), ax=axes[0, 1])
voltages = [100, 110, 120, 130, 150, 200]
figure_generator.s_parameter_lineplot(params_calculation['FreqS'], params_calculation['S11m'], voltages, 'S11', ylim=(viz_params['S11min'], viz_params['S11max']), ax=axes[1, 0])
figure_generator.s_parameter_lineplot(params_calculation['FreqS'], params_calculation['S21m'], voltages, 'S11', ylim=(viz_params['S21min'], viz_params['S21max']), ax=axes[1, 1])
plt.tight_layout()
plt.savefig('../datasets/Other_plots.png')
plt.close()
# plt.show()

# heatmaps
fig, axes = plt.subplots(3, 2, figsize=(10, 12))
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], params_calculation['Y12i'], plot_type='2d', title='Reactance', x_label='voltage', 
                              z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), ax=axes[0, 0])
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], params_calculation['Y12r'], plot_type='2d', title='Conductance', x_label='voltage', 
                              z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), ax=axes[0, 1])
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], params_calculation['Y11i'], plot_type='2d', title='Reactance', x_label='voltage', 
                              z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), ax=axes[1, 0])
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], params_calculation['Y11r'], plot_type='2d', title='Conductance', x_label='voltage', 
                              z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), ax=axes[1, 1])
figure_generator.plot_heatmap(params_calculation['V'], params_calculation['FreqS'], results['DiffConductance3D'], plot_type='2d', title='Difference in Conductance', x_label='voltage', 
                              z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, viz_params['FM']), ax=axes[2, 0])
fig.delaxes(axes[2, 1])
plt.tight_layout()
plt.savefig('../datasets/heatmaps.png')
plt.close()
# plt.show()
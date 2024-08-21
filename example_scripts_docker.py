import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
from src.rf_calculation import CapacitorAnalysis
from src.rf_figures import FigureGenerator
from src.utils import save_dict_to_hdf5, load_dict_from_hdf5

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def plot_codes_pack(output_folder, title):
    plt.tight_layout()
    logging.info(f"Saving file to: {os.path.join(output_folder, f'{title}.png')}")
    try:
        plt.savefig(os.path.join(output_folder, f'{title}.png'))
        logging.info("File saved successfully")
    except Exception as e:
        logging.error(f"Failed to save file: {str(e)}")
    plt.close()


def main(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)

    if not os.listdir(input_folder):
        print(f"Error: Input folder '{input_folder}' is empty.")
        sys.exit(1)
        
    os.makedirs(output_folder, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
    # print(f"Input folder: {input_folder}")
    # print(f"Contents of input folder:")
    # for root, dirs, files in os.walk(input_folder):
    #     for file in files:
    #         print(os.path.join(root, file))
            
    # Setup parameters and calculate
    params = {'VoltMax': 200, 'VoltStep': 2, 'DispIndex': 100, 'IDC_gap': 3e-4, 'CF': 0,
            'BVI': 101, 'FM': 26.5, 'FT': 32, 'LW': 1, 'QFSL': 10, 'QFSH': 10000, 'Cap3DL': 0.05, 'Cap3DH': 0.1,
            'TunL': 1, 'TunH': 2, 'LTmin': 0.01, 'LTmax': 0.5, 'S11min': -5, 'S11max': 0, 'S21min': -30, 'S21max': 0}

    analyzer = CapacitorAnalysis(params)
    params_calculation = analyzer.setup_params(folder_path=input_folder)
    results = analyzer.run_analysis()
    
    # logging.info(f"Saving file to: {os.path.join(output_folder, 'results.h5')}")
    # save_dict_to_hdf5(results, os.path.join(output_folder, 'results.h5'))
    # logging.info("File saved successfully")
    logging.info(f"Saving file to: {os.path.join(output_folder, 'results.h5')}")
    try:
        save_dict_to_hdf5(results, os.path.join(output_folder, 'results.h5'))
        logging.info("File saved successfully")
    except Exception as e:
        logging.error(f"Failed to save file: {str(e)}")
    
    # Visualization parameters
    figure_generator = FigureGenerator(params=results, figsize=(5,4), cmap='viridis')

    # Qfactor plots
    title = 'Qfactor'
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['QualityFactor'], plot_type='2d', title='Quality Factor', 
                                z_label='Q Factor', z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), 
                                ylim=(0.1, results['FM']), zlim=(results['QFSL'], results['QFSH']), ax=axes[0, 0])
    E_Field = (results['V'] / params['IDC_gap']) / 1000
    figure_generator.plot_heatmap(E_Field, results['FreqS'], results['QualityFactor'], plot_type='2d', title='Quality Factor', x_label='Field (kV/cm)', z_label='Q Factor', z_scale='log', 
                                xlim=(-(params['VoltMax']/params['IDC_gap'])/1000, (params['VoltMax']/params['IDC_gap'])/1000), 
                                ylim=(0.1, results['FM']), zlim=(results['QFSL'], results['QFSH']), ax=axes[0, 1])

    figure_generator.plot_heatmap(results['Vh'][1:], results['FreqS'], results['QFMF'].transpose(), plot_type='2d', title='Quality Factor', x_label='Positive_Voltage', z_label='Q Factor', z_scale='log',
                                zlim=(results['QFSL'], results['QFSH']), ax=axes[0, 2])
    figure_generator.Qfactor_lineplot(results['FreqS'], results['QualityFactor'], ax=axes[1, 0])
    bias_voltages = [(0, results['BVI']), (20, 110), (40, 120), (80, 140), (120, 160), (200, 200)]
    figure_generator.Qfactor_lineplot(results['FreqS'], results['QualityFactor'], bias_voltages, ax=axes[1, 1])
    figure_generator.Qfactor_peak_lineplot(results['FreqS'], results['QFFiltVolt'], ax=axes[1, 2])
    plot_codes_pack(output_folder, title)


    # Capacitance and conductance plots
    title = 'Capacitance'
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['Capacitance3D'], plot_type='2d', title='Capacitance', z_label='Capacitance (pF)', 
                                xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), zlim=(results['Cap3DL'], results['Cap3DH']), ax=axes[0])

    figure_generator.capacitance_lineplot(results['V'], results['FreqS'], results['Capacitance3D'], xaxis='voltage', fit_params=results, ax=axes[1])
    figure_generator.capacitance_lineplot(results['V'], results['FreqS'], results['Capacitance3D'], xaxis='field', fit_params=results, ax=axes[2])
    plot_codes_pack(output_folder, title)


    # Conductance plots
    title = 'Conductance'
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    figure_generator.plot_lineplot(results['FreqS'], np.abs(results['QualityFactor'][:, results['BVI']]), 
                                x_label='Frequency (GHz)', y_label='Quality Factor', title='Quality Factor @ 0 Bias', y_scale='log', ax=axes[0])
    figure_generator.capacitance_lineplot(results['V'], results['FreqS'], results['Capacitance3D'], xaxis='frequency', ax=axes[1])
    figure_generator.plot_lineplot(results['FreqS'], np.abs(results['Y12r'][:, results['BVI']]), 
                                x_label='Frequency (GHz)', y_label='Conductance (Siemens)', title='Conductance @ 0 Bias', y_scale='log', ax=axes[2])
    plot_codes_pack(output_folder, title)


    # Tunability plots
    title = 'Tunability'
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['Tunability3D'], plot_type='2d', title='Tunability Surface', 
                                xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), zlim=(results['TunL'], results['TunH']), ax=axes[0])
    figure_generator.plot_lineplot(results['FreqS'], results['Tunability2D'], x_label='Frequency (GHz)', y_label='Tunability', 
                                title='Tunability', x_scale='log', xlim=(0.1, results['FM']), ylim=(results['TunL'], results['TunH']), 
                                xticks=[0.1, 1, 10, 20], ax=axes[1])
    plot_codes_pack(output_folder, title)
    
    
    # Other plots
    title = 'Other_plots'
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    figure_generator.plot_lineplot(results['FreqS'], results['CQF'], x_label='Frequency (GHz)', y_label='CQF', title='CQF', 
                                y_scale='log', xlim=(0.1, 20), ylim=(min(results['CQF'])/1.1, max(results['CQF'])*1.1), xticks=[0.1, 1, 10, 20], ax=axes[0, 0])
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['LossTan'], plot_type='2d', title='Loss Tangent', z_label='Loss Tangent', z_scale='log', 
                                xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), zlim=(results['LTmin'], results['LTmax']), ax=axes[0, 1])
    voltages = [100, 110, 120, 130, 150, 200]
    figure_generator.s_parameter_lineplot(results['FreqS'], results['S11m'], voltages, 'S11', ylim=(results['S11min'], results['S11max']), ax=axes[1, 0])
    figure_generator.s_parameter_lineplot(results['FreqS'], results['S21m'], voltages, 'S11', ylim=(results['S21min'], results['S21max']), ax=axes[1, 1])
    plot_codes_pack(output_folder, title)

    
    # heatmaps
    title = 'Heatmaps'
    fig, axes = plt.subplots(3, 2, figsize=(10, 12))
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['Y12i'], plot_type='2d', title='Reactance', x_label='voltage', 
                                z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), ax=axes[0, 0])
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['Y12r'], plot_type='2d', title='Conductance', x_label='voltage', 
                                z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), ax=axes[0, 1])
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['Y11i'], plot_type='2d', title='Reactance', x_label='voltage', 
                                z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), ax=axes[1, 0])
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['Y11r'], plot_type='2d', title='Conductance', x_label='voltage', 
                                z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), ax=axes[1, 1])
    figure_generator.plot_heatmap(results['V'], results['FreqS'], results['DiffConductance3D'], plot_type='2d', title='Difference in Conductance', x_label='voltage', 
                                z_scale='log', xlim=(-params['VoltMax'], params['VoltMax']), ylim=(0.1, results['FM']), ax=axes[2, 0])
    fig.delaxes(axes[2, 1])
    plot_codes_pack(output_folder, title)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process RF data and generate plots.')
    parser.add_argument('--input_folder', type=str, default='/data/input', help='Path to the input folder containing S2P files')
    parser.add_argument('--output_folder', type=str, default='/data/output', help='Path to the output folder for results and plots')
    args = parser.parse_args()

    os.makedirs(args.output_folder, exist_ok=True)
    main(args.input_folder, args.output_folder)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from mpl_toolkits.mplot3d import Axes3D

class FigureGenerator:
    def __init__(self, params, figsize, cmap):
        self.params = params
        print('FigureGenerator: Initialized')
        
        self.VoltMax = params['VoltMax']
        # self.V = params['V']
        self.QFSL = params['QFSL']
        self.QFSH = params['QFSH']
        self.FM = params['FM']
        self.IDC_gap = params['IDC_gap']
        
        # self.QFMF = self.params['QFMF']
        self.BVI = params['BVI']
        self.LW = params['LW']
        self.FT = params['FT']
        self.TunL = params['TunL']
        self.TunH = params['TunH']
        self.LTmin = params['LTmin']
        self.LTmax = params['LTmax']
        
        self.cmap = cmap
        self.figsize = figsize
        
        
    # heatmap
    def plot_heatmap(self, x_data, y_data, z_data, plot_type='2d', x_label='Bias Voltage', y_label='Frequency (GHz)', 
                     title='', z_label='', x_scale='linear', y_scale='linear', z_scale='linear', 
                     xlim=None, ylim=None, zlim=None, norm=True, figsize=None):
        """
        A unified function to plot various heatmaps and 3D surfaces.
        
        :param x_data: 1D array for x-axis data
        :param y_data: 1D array for y-axis data
        :param z_data: 2D array for z-axis data
        :param plot_type: '2d' for heatmap or '3d' for surface plot (default: '2d')
        :param x_label: Label for x-axis (default: 'Bias Voltage')
        :param y_label: Label for y-axis (default: 'Frequency (GHz)')
        :param title: Plot title
        :param z_label: Label for z-axis or colorbar
        :param x_scale: Scale for x-axis ('linear' or 'log')
        :param y_scale: Scale for y-axis ('linear' or 'log')
        :param z_scale: Scale for z-axis or colorbar ('linear' or 'log')
        :param zlim[0]: Minimum value for colormap
        :param v_max: Maximum value for colormap
        :param figsize: Optional tuple specifying figure size
        """
        if x_data is None or y_data is None or z_data is None:
            raise ValueError('x_data, y_data, and z_data must be provided')
        
        if figsize is None:
            figsize = self.figsize
        
        fig = plt.figure(figsize=figsize)
        
        if plot_type == '2d':
            ax = fig.add_subplot(111)
            if zlim != None:
                norm = LogNorm(vmin=zlim[0], vmax=zlim[1]) if z_scale == 'log' else Normalize(vmin=zlim[0], vmax=zlim[1])
            else:
                norm = None
            im = ax.pcolormesh(x_data, y_data, z_data, cmap=self.cmap, norm=norm, shading='auto')
            plt.colorbar(im, label=z_label)
        elif plot_type == '3d':
            ax = fig.add_subplot(111, projection='3d')
            X, Y = np.meshgrid(x_data, y_data)
            if zlim != None and norm:
                norm = LogNorm(vmin=zlim[0], vmax=zlim[1]) if z_scale == 'log' else Normalize(vmin=zlim[0], vmax=zlim[1])
            else:
                norm = None
            surf = ax.plot_surface(X, Y, z_data, cmap=self.cmap, norm=norm)
            # ax.set_zlabel(z_label)
            ax.view_init(elev=30, azim=-45)
            plt.colorbar(surf, label=z_label)
            if zlim:
                ax.set_zlim(zlim)
        else:
            raise ValueError("plot_type must be either '2d' or '3d'")
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        
        if x_scale == 'log':
            ax.set_xscale('log')
        if y_scale == 'log':
            ax.set_yscale('log')
        
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)
        ax.tick_params(axis='both', which='major')
        plt.tight_layout()
        plt.show()
        
        
    def plot_lineplot(self, x_data, y_data, x_label='', y_label='', title='', 
                    x_scale='linear', y_scale='linear', xlim=None, ylim=None, 
                    xticks=None, figsize=None, color='k'):
        """
        A unified function to plot various line plots.
        
        :param x_data: 1D array for x-axis data
        :param y_data: 1D array for y-axis data
        :param plot_type: String indicating the type of plot ('conductance', 'tunability', or 'cqf')
        :param x_label: Label for x-axis
        :param y_label: Label for y-axis
        :param title: Plot title
        :param x_scale: Scale for x-axis ('linear' or 'log')
        :param y_scale: Scale for y-axis ('linear' or 'log')
        :param xlim: Tuple for x-axis limits (min, max)
        :param ylim: Tuple for y-axis limits (min, max)
        :param xticks: List of x-axis tick locations
        :param figsize: Optional tuple specifying figure size
        :param color: Color of the plot line
        """
        if x_data is None or y_data is None:
            raise ValueError('x_data and y_data must be provided')
        
        if figsize is None:
            figsize = self.figsize
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(x_data, y_data, color=color, linewidth=self.LW)
        
        ax.set_xscale(x_scale)
        ax.set_yscale(y_scale)
        
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)
        
        if xticks:
            ax.set_xticks(xticks)
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        
        plt.tight_layout()
        plt.show()
        
        
    def Qfactor_lineplot(self, FreqS, QualityFactor, bias_voltages=None, figsize=None):
        """
        Plots Quality Factor vs Frequency for one or multiple bias voltages.
        
        :param FreqS: 1D array of frequency values
        :param QualityFactor: 2D array of Quality Factor values
        :param bias_voltages: List of tuples (voltage, index) or None for default 0V plot
        """
        if figsize is None:
            figsize = self.figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
                
        if bias_voltages is None:
            # Default to plotting only at 0V (specific bias case)
            plt.plot(FreqS, QualityFactor[:, self.BVI], 'k', linewidth=self.LW, label='0V')
            title = 'Quality Factor @ 0 Volts'
        else:
            # Plot for various biases
            colors = ['k', 'r', 'g', 'b', 'c', 'm']  # Add more colors if needed
            for i, (voltage, index) in enumerate(bias_voltages):
                color = colors[i % len(colors)]  # Cycle through colors if more voltages than colors
                plt.plot(FreqS, QualityFactor[:, index], color, linewidth=self.LW, label=f'{voltage}V')
            title = 'Quality Factor at Various Bias Voltages'
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(min(FreqS), self.FM)
        plt.ylim(0, np.max(QualityFactor))
        plt.xticks([0.1, 1, 5, 10, 20])
        plt.xlabel('Frequency')
        plt.ylabel('Q Factor')
        plt.title(title)
        
        if bias_voltages is not None:
            plt.legend()
        
        plt.show()
        
        
    def Qfactor_peak_lineplot(self, FreqS, QFFiltVolt, figsize=None):
        if figsize is None:
            figsize = self.figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        plt.plot(FreqS, QFFiltVolt, 'k', linewidth=self.LW)
        plt.xlim(0.1, self.FM)
        plt.ylim(0, self.VoltMax*1.1)
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Bias Voltage')
        plt.title('Quality Factor Peak at Individual Frequencies')
        plt.show()
        

        
    # capacitance
    def capacitance_lineplot(self, V, FreqS, Capacitance3D, xaxis='voltage', fit_params=None, figsize=None):
        """
        Plots 2D Capacitance with different x-axes based on the plot type.
        
        :param V: 1D array of voltage values
        :param FreqS: 1D array of frequency values
        :param Capacitance3D: 2D array of capacitance values
        :param xaxis: String, either 'voltage', 'field', or 'frequency'
        """
        if V is None or FreqS is None or Capacitance3D is None:
            raise ValueError('Voltage, Frequency, and Capacitance data must be provided')
        
        if figsize is None:
            figsize = self.figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
                
        if xaxis == 'voltage':
            plt.plot(V, Capacitance3D[self.params['DispIndex'],:], 'k', linewidth=self.LW)
            
            if not isinstance(fit_params, type(None)):
                label = f'Fit: C_max={fit_params["Cmax_fitted"]:.2e}, V_1/2={fit_params["V_half_fitted"]:.2f}, C_f={fit_params["Cf_fitted"]:.2e}'
                plt.plot(fit_params['V_fit'], fit_params['C_fit'], label=label, linewidth=self.LW, linestyle='--')
                plt.legend()

            plt.xlim(-self.params['VoltMax'], self.params['VoltMax'])
            plt.xlabel('Bias Voltage')
            plt.title('Capacitance @1GHz')
            
        elif xaxis == 'field':
            E_Field = (V / self.params['IDC_gap']) / 1000
            plt.plot(E_Field, Capacitance3D[self.params['DispIndex'],:], 'k', linewidth=self.LW)
            
            if not isinstance(fit_params, type(None)):
                E_Field_fit = (fit_params['V_fit'] / self.params['IDC_gap']) / 1000
                label = f'Fit: C_max={fit_params["Cmax_fitted"]:.2e}, V_1/2={fit_params["V_half_fitted"]:.2f}, C_f={fit_params["Cf_fitted"]:.2e}'
                plt.plot(E_Field_fit, fit_params['C_fit'], label=label, linewidth=self.LW, linestyle='--')
                plt.legend()
                
            plt.xlim(-(self.params['VoltMax']/self.params['IDC_gap'])/1000, (self.params['VoltMax']/self.params['IDC_gap'])/1000)
            plt.xlabel('Field (kV/cm)')
            plt.title('Capacitance @1GHz')
            
        elif xaxis == 'frequency':
            plt.plot(FreqS, Capacitance3D[:,self.params['BVI']], 'k', linewidth=self.LW)
            plt.xlim(0, max(FreqS))
            plt.ylim(0, max(Capacitance3D[:,self.params['BVI']]) * 1.1)
            plt.xlabel('Frequency (GHz)')
            plt.title('Capacitance @ 0 Bias')
        
        else:
            raise ValueError('Invalid plot type. Choose "voltage", "field", or "frequency".')
        
        plt.ylabel('Capacitance (pF)')
        plt.tick_params(axis='both', which='major')
        plt.tight_layout()
        plt.show()        
        
        
    def compare_conductance_capacitance(self, FreqS, QualityFactor, Capacitance3D, Y12r, figsize=None):
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Quality Factor plot
        axes[0].plot(FreqS, QualityFactor[:, self.BVI], 'k', linewidth=self.LW)
        axes[0].set_yscale('log')
        axes[0].set_xlabel('Frequency (GHz)')
        axes[0].set_ylabel('Q Factor')
        axes[0].set_title('Quality Factor @ 0 Bias')

        # Capacitance plot
        axes[1].plot(FreqS, Capacitance3D[:, self.BVI], 'k', linewidth=self.LW)
        axes[1].set_xlim(0, max(FreqS))
        axes[1].set_ylim(0, max(Capacitance3D[:, self.BVI])*1.1)
        axes[1].set_xlabel('Frequency (GHz)')
        axes[1].set_ylabel('Capacitance (pF)')
        axes[1].set_title('Capacitance @ 0 Bias')

        # Conductance plot
        axes[2].plot(FreqS, np.abs(Y12r[:, self.BVI]), 'k', linewidth=self.LW)
        axes[2].set_yscale('log')
        axes[2].set_xlabel('Frequency (GHz)')
        axes[2].set_ylabel('Conductance (Siemens)')
        axes[2].set_title('Conductance @ 0 Bias')

        plt.suptitle('Conductance and Capacitance Comparison', fontsize=16)
        plt.tight_layout()
        plt.show()
            
        
            
            
    def tunability_lineplot(self, FreqS, Tunability2D):
        plt.figure(figsize=self.figsize)
        plt.plot(FreqS, Tunability2D, 'k', linewidth=self.LW)
        plt.xlim(0.1, self.FM)
        plt.ylim(self.TunL, self.TunH)
        plt.xscale('log')
        plt.xticks([0.1, 1, 10, 20])
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Tunability')
        plt.title('Tunability')
        
        plt.show()
        

    def cqf_lineplot(self, FreqS, CQF):
        """
        Plots CQF vs Frequency.
        
        :param FreqS: 1D array of frequency values
        :param CQF: 1D array of CQF values
        """
        if FreqS is None or CQF is None:
            raise ValueError('Frequency and CQF data must be provided')
        
        plt.figure(figsize=self.figsize)
        plt.plot(FreqS, CQF, 'k', linewidth=self.LW)
        plt.xlim(0.1, 20)
        plt.ylim(min(CQF)/1.1, max(CQF)*1.1)
        plt.xscale('log')
        plt.yscale('log')
        plt.xticks([0.1, 1, 10, 20])
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('CQF')
        plt.title('CQF')
        plt.tight_layout()
        plt.show()

    def loss_tangent_heatmap(self, V, FreqS, LossTan):
        """
        Plots a 3D surface of Loss Tangent.
        
        :param FreqS: 1D array of frequency values
        :param LossTan: 2D array of loss tangent values
        :param LTmin: Minimum value for loss tangent
        :param LTmax: Maximum value for loss tangent
        """
        if V is None or FreqS is None or LossTan is None:
            raise ValueError('Voltage, Frequency, and Loss Tangent data must be provided')
        
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        X, Y = np.meshgrid(V, FreqS)
        surf = ax.plot_surface(X, Y, LossTan, cmap=self.cmap, norm=LogNorm(vmin=self.LTmin, vmax=self.LTmax))
        
        ax.set_xlim(-self.VoltMax, self.VoltMax)
        ax.set_ylim(0.1, self.FM)
        ax.view_init(0, 90)
        ax.set_xlabel('Bias Voltage')
        ax.set_ylabel('Frequency (GHz)')
        ax.set_zlabel('Loss Tangent')
        ax.set_title('Loss Tangent')
        plt.colorbar(surf, label='Loss Tangent')
        plt.tight_layout()
        plt.show()
        

    def s_parameters_lineplot(self, FreqS, S11m, S21m, voltages, S11min, S11max, S21min, S21max):
        """
        Plots S-parameters (S11 and S21) vs Frequency for various voltages.
        
        :param FreqS: 1D array of frequency values
        :param S11m: 2D array of S11 magnitudes
        :param S21m: 2D array of S21 magnitudes
        :param S11min, S11max: Y-axis limits for S11 plot
        :param S21min, S21max: Y-axis limits for S21 plot
        """
        if FreqS is None or S11m is None or S21m is None:
            raise ValueError('Frequency and S-parameter data must be provided')

        # voltages = [100, 105, 110, 115, 120, 130, 140, 150, 175, 200]
        # voltages = [100, 110, 120, 130, 150, 200]
        colors = plt.get_cmap(self.cmap)(np.linspace(0, 1, len(voltages)))
        
        fig, axes = plt.subplots(1, 2, figsize=(self.figsize[0]*2, self.figsize[1]))
        
        handles = []
        for v, c in zip(voltages, colors):
            line, = axes[0].plot(FreqS, S11m[:, v], c=c, linewidth=self.LW)
            handles.append(line)
        axes[0].set_xlim(0, self.FM)
        axes[0].set_ylim(S11min, S11max)
        axes[0].set_xlabel('Frequency (GHz)')
        axes[0].set_ylabel('Magnitude (dB)')
        axes[0].set_title('S_11')
        axes[0].legend(handles, [f'{v}V' for v in voltages])

        for v, c in zip(voltages, colors):
            axes[1].plot(FreqS, S21m[:, v], c=c, linewidth=self.LW)
        axes[1].set_xlim(0, self.FM)
        axes[1].set_ylim(S21min, S21max)
        axes[1].set_xlabel('Frequency (GHz)')
        axes[1].set_ylabel('Magnitude (dB)')
        axes[1].set_title('S_21')
        axes[1].legend(handles, [f'{v}V' for v in voltages])

        plt.tight_layout()
        plt.show()   
        
        
        

        
    # ## conductance
    # def conductance_lineplot(self, FreqS, Y12r, figsize=None):
    #     if figsize is None:
    #         figsize = self.figsize
    #     fig, ax = plt.subplots(1, 1, figsize=figsize)
    #     plt.plot(FreqS, np.abs(Y12r[:, self.BVI]), 'k', linewidth=self.LW)
    #     # plt.xlim(0, self.FM)
    #     # plt.ylim(0, max(np.abs(Y12r[:, self.BVI]))*1.1)
    #     plt.yscale('log')
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('Conductance (Siemens)')
    #     plt.title('Conductance @ 0 Bias')
    #     plt.show()



    # def generate_y_parameter_plots(self, V, FreqS, Y12i, Y12Conductance3D, Y11i, Y11Conductance3D):
    #     """
    #     Plots Y-parameters (Y12 and Y11, both real and imaginary parts) in 3D.
        
    #     :param V: 1D array of voltage values
    #     :param FreqS: 1D array of frequency values
    #     :param Y12i: 2D array of Y12 imaginary values
    #     :param Y12Conductance3D: 2D array of Y12 real values
    #     :param Y11i: 2D array of Y11 imaginary values
    #     :param Y11Conductance3D: 2D array of Y11 real values
    #     """
    #     if V is None or FreqS is None or Y12i is None or Y12Conductance3D is None or Y11i is None or Y11Conductance3D is None:
    #         raise ValueError('Voltage, Frequency, and Y-parameter data must be provided')

    #     X, Y = np.meshgrid(V, FreqS)

    #     for data, title in zip([np.abs(Y12i), Y12Conductance3D, np.abs(Y11i), Y11Conductance3D],
    #                            ['Y12 Imaginary', 'Y12 Real', 'Y11 Imaginary', 'Y11 Real']):
    #         fig = plt.figure(figsize=self.figsize)
    #         ax = fig.add_subplot(111, projection='3d')
    #         surf = ax.plot_surface(X, Y, data, cmap=self.cmap, norm=LogNorm())
    #         ax.set_xlim(-self.VoltMax, self.VoltMax)
    #         ax.set_ylim(0.1, self.FM)
    #         ax.view_init(0, 90)
    #         ax.set_xlabel('Bias Voltage')
    #         ax.set_ylabel('Frequency (GHz)')
    #         ax.set_zlabel('Reactance' if 'Imaginary' in title else 'Conductance (Siemens)')
    #         ax.set_title(title)
    #         plt.colorbar(surf)
    #         plt.tight_layout()
    #         plt.show()


    # def generate_difference_in_conduction_plot(self, V, FreqS, DiffConductance3D):
    #     """
    #     Plots the difference in conductance in 3D.
        
    #     :param V: 1D array of voltage values
    #     :param FreqS: 1D array of frequency values
    #     :param DiffConductance3D: 2D array of difference in conductance values
    #     """
    #     if V is None or FreqS is None or DiffConductance3D is None:
    #         raise ValueError('Voltage, Frequency, and Difference in Conductance data must be provided')

    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     X, Y = np.meshgrid(V, FreqS)
    #     surf = ax.plot_surface(X, Y, np.abs(DiffConductance3D), cmap=self.cmap, norm=LogNorm())
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Difference in Conductance')
    #     ax.set_title('Difference in Conductance')
    #     plt.colorbar(surf)
    #     plt.tight_layout()
    #     plt.show()

    # def generate_rfplot(self, FreqS, S, S11min, S11max, S21min, S21max):
    #     """
    #     Plots RF parameters (S11 and S21) for various voltages.
        
    #     :param FreqS: 1D array of frequency values
    #     :param S: 4D array of S-parameters
    #     :param S11min, S11max: Y-axis limits for S11 plot
    #     :param S21min, S21max: Y-axis limits for S21 plot
    #     """
    #     if FreqS is None or S is None:
    #         raise ValueError('Frequency and S-parameter data must be provided')

    #     voltages = [0, 10, 20, 30, 40, 60, 80, 100, 150, 200]
    #     colors = ['r', 'g', 'b', 'y', 'c', 'm', (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (0.5, 0.5, 0)]

    #     plt.figure(figsize=self.figsize)
    #     for s, color, voltage in zip([S[100], S[105], S[110], S[115], S[120], S[130], S[140], S[150], S[175], S[200]], colors, voltages):
    #         plt.plot(FreqS, np.abs(s[:, 0, 0]), color=color, linewidth=self.LW, label=f'{voltage}V')
    #     plt.xlim(0, self.FM)
    #     plt.ylim(S11min, S11max)
    #     plt.title('S_{11}')
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('S_{11} (dB)')
    #     plt.legend()
    #     plt.tight_layout()
    #     plt.show()

    #     plt.figure(figsize=self.figsize)
    #     for s, color, voltage in zip([S[100], S[105], S[110], S[115], S[120], S[130], S[140], S[150], S[175], S[200]], colors, voltages):
    #         plt.plot(FreqS, np.abs(s[:, 1, 0]), color=color, linewidth=self.LW, label=f'{voltage}V')
    #     plt.xlim(0, self.FM)
    #     plt.ylim(S21min, S21max)
    #     plt.title('S_{21}')
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('S_{21} (dB)')
    #     plt.legend()
    #     plt.tight_layout()
    #     plt.show()
        
        
            
            
            
        
        

    # ## Qfactor
    # def Qfactor_heatmap(self, V, FreqS, QualityFactor, xaxis='Voltage', yaxis='Frequency', log_y=False, figsize=None):
    #     """
    #     Plots Quality Factor with different x, y axes based on the plot type.
        
    #     :param plot_type: String, either 'voltage', 'field', or 'positive'
    #     :param x_data: 1D array for x-axis data
    #     :param y_data: 1D array for y-axis data
    #     :param z_data: 2D array for z-axis data (QualityFactor or QFMF)
    #     :param self.params: Dictionary containing additional parameters
    #     """
    #     if V is None or FreqS is None or QualityFactor is None:
    #             raise ValueError('Voltage, Frequency, and QualityFactor data must be provided')
            
    #     if figsize is None:
    #         figsize = self.figsize
    #     fig, ax = plt.subplots(1, 1, figsize=figsize)
                
    #     if xaxis=='Voltage' and yaxis=='Frequency':
    #         im = ax.pcolormesh(V, FreqS, QualityFactor, 
    #                         norm=LogNorm(vmin=self.params['QFSL'], vmax=self.params['QFSH']),
    #                         cmap=self.cmap, shading='auto')
    #         ax.set_xlim(-self.params['VoltMax'], self.params['VoltMax'])
    #         ax.set_ylim(0.1, self.params['FM'])
    #         ax.set_xlabel('Bias Voltage')
    #         ax.set_ylabel('Frequency (GHz)')
    #         ax.set_title('Quality Factor')
    #         # Remove the following line if it exists:
    #         # ax.set_yscale('log')
            
    #     elif xaxis=='E_Field' and yaxis=='Frequency':

    #         E_Field = (V / self.params['IDC_gap']) / 1000
    #         im = ax.pcolormesh(E_Field, FreqS, QualityFactor, norm=LogNorm(vmin=self.params['QFSL'], vmax=self.params['QFSH']),
    #                         cmap=self.cmap, shading='auto')
    #         ax.set_xlim(-(self.params['VoltMax']/self.params['IDC_gap'])/1000, (self.params['VoltMax']/self.params['IDC_gap'])/1000)
    #         ax.set_ylim(0.1, self.params['FM'])
    #         ax.set_xlabel('Field (kV/cm)')
    #         ax.set_ylabel('Frequency (GHz)')
    #         ax.set_title('Quality Factor (Electric Field)')
            
    #     elif xaxis=='Frequency' and yaxis=='Positive_Voltage':
    #         im = ax.pcolormesh(V, FreqS, QualityFactor, norm=LogNorm(vmin=self.params['QFSL'], vmax=self.params['QFSH']),
    #                         cmap=self.cmap, shading='auto')
    #         ax.set_xlim(0, self.params['VoltMax'])
    #         ax.set_ylim(0.1, self.params['FM'])
    #         ax.set_xlabel('Bias Voltage')
    #         ax.set_ylabel('Frequency (GHz)')
    #         ax.set_title('Quality Factor (Positive Voltage Bias)')
    #     else:
    #         raise ValueError('Invalid x-axis and y-axis combination')
        
    #     if log_y:
    #         ax.set_yscale('log')
    #     plt.colorbar(im, label='Q Factor')
    #     plt.tight_layout()
    #     plt.show()


        
    # ## capacitance
    # def capacitance_heatmap_3d(self, V, FreqS, Capacitance3D, figsize=None):
    #     """
    #     Plots a 3D surface of Capacitance.
        
    #     :param V: 1D array of voltage values
    #     :param FreqS: 1D array of frequency values
    #     :param Capacitance3D: 2D array of capacitance values
    #     """
    #     if V is None or FreqS is None or Capacitance3D is None:
    #         raise ValueError('Voltage, Frequency, and Capacitance data must be provided')
        
    #     if figsize is None:
    #         figsize = self.figsize
    #     fig, ax = plt.subplots(1, 1, figsize=figsize)
    #     ax = fig.add_subplot(111, projection='3d')
        
    #     X, Y = np.meshgrid(V, FreqS)
    #     surf = ax.plot_surface(X, Y, Capacitance3D, cmap=self.cmap, shade=True)
        
    #     ax.set_xlim(-self.params['VoltMax'], self.params['VoltMax'])
    #     ax.set_ylim(0.1, self.params['FM'])
    #     ax.set_zlim(self.params['Cap3DL'], self.params['Cap3DH'])
    #     ax.view_init(elev=30, azim=-45)
        
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Capacitance (pF)')
    #     ax.set_title('Capacitance')
    #     ax.tick_params(axis='both', which='major')
    #     plt.colorbar(surf, label='Capacitance (pF)')
    #     plt.tight_layout()
    #     plt.show()
        
        
    # def capacitance_heatmap(self, V, FreqS, Capacitance3D, figsize=None):
    #     """
    #     Plots a heatmap of Capacitance.
        
    #     :param V: 1D array of voltage values
    #     :param FreqS: 1D array of frequency values
    #     :param Capacitance3D: 2D array of capacitance values
    #     """
    #     if V is None or FreqS is None or Capacitance3D is None:
    #         raise ValueError('Voltage, Frequency, and Capacitance data must be provided')
        
    #     if figsize is None:
    #         figsize = self.figsize
    #     fig, ax = plt.subplots(1, 1, figsize=figsize)
                
    #     im = ax.pcolormesh(V, FreqS, Capacitance3D, 
    #                        norm=Normalize(vmin=self.params['Cap3DL'], vmax=self.params['Cap3DH']),
    #                        cmap=self.cmap, shading='auto')
        
    #     ax.set_xlim(-self.params['VoltMax'], self.params['VoltMax'])
    #     ax.set_ylim(0.1, self.params['FM'])
        
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_title('Capacitance')
        
    #     plt.colorbar(im, label='Capacitance (pF)')
        
    #     ax.tick_params(axis='both', which='major', labelsize=self.params['FT'])
        
    #     plt.tight_layout()
    #     plt.show()
        

    # # tunability    
    # def tunability_heatmap_3d(self, V, FreqS, Tunability3D, figsize=None):
    #     """
    #     Plots a 3D surface of Tunability.
        
    #     :param FreqS: 1D array of frequency values
    #     :param Tunability3D: 2D array of tunability values
    #     """
    #     if V is None or FreqS is None or Tunability3D is None:
    #         raise ValueError('Voltage, Frequency, and Tunability data must be provided')
        
    #     if figsize is None:
    #         figsize = self.figsize
    #     fig, ax = plt.subplots(1, 1, figsize=figsize)
    #     ax = fig.add_subplot(111, projection='3d')
        
    #     X, Y = np.meshgrid(V, FreqS)
    #     surf = ax.plot_surface(X, Y, Tunability3D, cmap=self.cmap, shade=True)
        
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.set_zlim(self.TunL, self.TunH)
    #     ax.view_init(elev=30, azim=-45)
        
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Tunability')
    #     ax.set_title('Tunability')
    #     ax.tick_params(axis='both', which='major')
    #     plt.colorbar(surf, label='Tunability')
    #     plt.tight_layout()
    #     plt.show()
        
        
        
        
        
    # def tunability_heatmap(self, V, FreqS, Tunability3D, plot_type='2d', figsize=None):
    #     """
    #     Plots Tunability data in either 2D or 3D.
        
    #     :param V: 1D array of voltage values
    #     :param FreqS: 1D array of frequency values
    #     :param Tunability3D: 2D array of tunability values
    #     :param plot_type: '2d' for heatmap or '3d' for surface plot (default: '2d')
    #     :param figsize: Optional tuple specifying figure size
    #     """
    #     if V is None or FreqS is None or Tunability3D is None:
    #         raise ValueError('Voltage, Frequency, and Tunability data must be provided')
        
    #     if figsize is None:
    #         figsize = self.figsize
        
    #     fig = plt.figure(figsize=figsize)
        
    #     if plot_type == '2d':
    #         ax = fig.add_subplot(111)
    #         im = ax.pcolormesh(V, FreqS, Tunability3D, 
    #                         cmap=self.cmap, 
    #                         shading='auto',
    #                         norm=plt.Normalize(vmin=self.TunL, vmax=self.TunH))
            
    #         cbar = plt.colorbar(im, ax=ax)
    #         cbar.set_label('Tunability')
            
    #     elif plot_type == '3d':
    #         ax = fig.add_subplot(111, projection='3d')
    #         X, Y = np.meshgrid(V, FreqS)
    #         surf = ax.plot_surface(X, Y, Tunability3D, cmap=self.cmap, shade=True)
            
    #         ax.set_zlim(self.TunL, self.TunH)
    #         ax.set_zlabel('Tunability')
    #         ax.view_init(elev=30, azim=-45)
            
    #         plt.colorbar(surf, label='Tunability')
            
    #     else:
    #         raise ValueError("plot_type must be either '2d' or '3d'")
        
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_title('Tunability ' + ('Heatmap' if plot_type == '2d' else 'Surface'))
        
    #     ax.tick_params(axis='both', which='major')
    #     plt.tight_layout()
    #     plt.show()
        
        
        
        
        
        

    # def generate_cqf_plot(self, FreqS, CQF):
    #     plt.figure(figsize=self.figsize)
    #     plt.plot(FreqS, CQF, 'k', linewidth=self.LW)
    #     plt.xlim(0.1, 20)
    #     plt.ylim(min(CQF)/1.1, max(CQF)*1.1)
    #     plt.xscale('log')
    #     plt.yscale('log')
    #     plt.xticks([0.1, 1, 10, 20])
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('CQF')
    #     plt.title('CQF')
    #     plt.show()

    # def generate_loss_tangent_plot(self, FreqS, LossTan, LTmin, LTmax):
    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     surf = ax.plot_surface(self.V, FreqS, LossTan, cmap=self.cmap, norm=LogNorm(vmin=LTmin, vmax=LTmax))
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Loss Tangent')
    #     ax.set_title('Loss Tangent')
    #     fig.colorbar(surf)
    #     plt.show()

    # def generate_s_parameters_plot(self, FreqS, S11m, S21m, S11min, S11max, S21min, S21max):
    #     plt.figure(figsize=self.figsize)
    #     plt.plot(FreqS, S11m[:, 100], 'k', linewidth=self.LW, label='0V')
    #     plt.plot(FreqS, S11m[:, 110], 'r', linewidth=self.LW, label='20V')
    #     plt.plot(FreqS, S11m[:, 125], 'b', linewidth=self.LW, label='50V')
    #     plt.plot(FreqS, S11m[:, 140], 'g', linewidth=self.LW, label='80V')
    #     plt.plot(FreqS, S11m[:, 165], 'c', linewidth=self.LW, label='130V')
    #     plt.plot(FreqS, S11m[:, 200], 'm', linewidth=self.LW, label='200V')
    #     plt.xlim(0, self.FM)
    #     plt.ylim(S11min, S11max)
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('Magnitude (dB)')
    #     plt.title('S_{11}')
    #     plt.legend()
    #     plt.show()

    #     plt.figure(figsize=self.figsize)
    #     plt.plot(FreqS, S21m[:, 100], 'k', linewidth=self.LW, label='0V')
    #     plt.plot(FreqS, S21m[:, 110], 'r', linewidth=self.LW, label='20V')
    #     plt.plot(FreqS, S21m[:, 125], 'b', linewidth=self.LW, label='50V')
    #     plt.plot(FreqS, S21m[:, 140], 'g', linewidth=self.LW, label='80V')
    #     plt.plot(FreqS, S21m[:, 165], 'c', linewidth=self.LW, label='130V')
    #     plt.plot(FreqS, S21m[:, 200], 'm', linewidth=self.LW, label='200V')
    #     plt.xlim(0, self.FM)
    #     plt.ylim(S21min, S21max)
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('Magnitude (dB)')
    #     plt.title('S_{21}')
    #     plt.legend()
    #     plt.show()

    # def generate_y_parameter_plots(self, FreqS, Y12i, Y12Conductance3D, Y11i, Y11Conductance3D):
    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     surf = ax.plot_surface(self.V, FreqS, np.abs(Y12i), cmap=self.cmap, norm=LogNorm())
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Reactance')
    #     ax.set_title('Y12 Imaginary')
    #     fig.colorbar(surf)
    #     plt.show()

    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     surf = ax.plot_surface(self.V, FreqS, Y12Conductance3D, cmap=self.cmap, norm=LogNorm())
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Conductance (Siemens)')
    #     ax.set_title('Y12 Real')
    #     fig.colorbar(surf)
    #     plt.show()

    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     surf = ax.plot_surface(self.V, FreqS, np.abs(Y11i), cmap=self.cmap, norm=LogNorm())
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Reactance')
    #     ax.set_title('Y11 Imaginary')
    #     fig.colorbar(surf)
    #     plt.show()

    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     surf = ax.plot_surface(self.V, FreqS, Y11Conductance3D, cmap=self.cmap, norm=LogNorm())
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Conductance (Siemens)')
    #     ax.set_title('Y11 Real')
    #     fig.colorbar(surf)
    #     plt.show()

    # def generate_difference_in_conduction_plot(self, FreqS, DiffConductance3D):
    #     fig = plt.figure(figsize=self.figsize)
    #     ax = fig.add_subplot(111, projection='3d')
    #     surf = ax.plot_surface(self.V, FreqS, np.abs(DiffConductance3D), cmap=self.cmap, norm=LogNorm())
    #     ax.set_xlim(-self.VoltMax, self.VoltMax)
    #     ax.set_ylim(0.1, self.FM)
    #     ax.view_init(0, 90)
    #     ax.set_xlabel('Bias Voltage')
    #     ax.set_ylabel('Frequency (GHz)')
    #     ax.set_zlabel('Difference in Conductance')
    #     ax.set_title('Difference in Conductance')
    #     fig.colorbar(surf)
    #     plt.show()

    # def generate_rfplot(self, FreqS, S, S11min, S11max, S21min, S21max):
    #     # S11 Plots
    #     plt.figure(figsize=self.figsize)
    #     colors = ['r', 'g', 'b', 'y', 'c', 'm', (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5), (0.5, 0.5, 0)]
    #     voltages = [0, 10, 20, 30, 40, 60, 80, 100, 150, 200]
    #     for s, color, voltage in zip([S[100], S[105], S[110], S[115], S[120], S[130], S[140], S[150], S[175], S[200]], colors, voltages):
    #         plt.plot(FreqS, np.abs(s[:, 0, 0]), color=color, linewidth=self.LW, label=f'{voltage}V')
    #     plt.xlim(0, self.FM)
    #     plt.ylim(S11min, S11max)
    #     plt.title('S_{11}')
    #     plt.xlabel('Frequency (GHz)')
    #     plt.ylabel('S_{11} (dB)')
    #     plt.legend()
    #     plt.show()

        # # S21 Plots
        # plt.figure(figsize=self.figsize)
        # for s, color, voltage in zip([S[100], S[105], S[110], S[115], S[120], S[130], S[140], S[150], S[175], S[200]], colors, voltages):
        #     plt.plot(FreqS, np.abs(s[:, 1, 0]), color=color, linewidth=self.LW, label=f'{voltage}V')
        # plt.xlim(0, self.FM)
        # plt.ylim(S21min, S21max)
        # plt.title('S_{21}')
        # plt.xlabel('Frequency (GHz)')
        # plt.ylabel('S_{21} (dB)')
        # plt.legend()
        # plt.show()
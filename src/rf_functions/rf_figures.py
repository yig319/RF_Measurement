import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize

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
                     xlim=None, ylim=None, zlim=None, norm=True, figsize=None, ax=None):
        if x_data is None or y_data is None or z_data is None:
            raise ValueError('x_data, y_data, and z_data must be provided')
        
        if figsize is None:
            figsize = self.figsize
        
        if ax is None:
            fig = plt.figure(figsize=figsize)
            if plot_type == '2d':
                ax = fig.add_subplot(111)
            elif plot_type == '3d':
                ax = fig.add_subplot(111, projection='3d')
            else:
                raise ValueError("plot_type must be either '2d' or '3d'")
        else:
            fig = ax.figure
        
        if plot_type == '2d':
            if zlim != None:
                norm = LogNorm(vmin=zlim[0], vmax=zlim[1]) if z_scale == 'log' else Normalize(vmin=zlim[0], vmax=zlim[1])
            else:
                norm = None
            im = ax.pcolormesh(x_data, y_data, z_data, cmap=self.cmap, norm=norm, shading='auto')
            plt.colorbar(im, label=z_label, ax=ax)
        elif plot_type == '3d':
            X, Y = np.meshgrid(x_data, y_data)
            if zlim != None and norm:
                norm = LogNorm(vmin=zlim[0], vmax=zlim[1]) if z_scale == 'log' else Normalize(vmin=zlim[0], vmax=zlim[1])
            else:
                norm = None
            surf = ax.plot_surface(X, Y, z_data, cmap=self.cmap, norm=norm)
            ax.view_init(elev=30, azim=-45)
            plt.colorbar(surf, label=z_label, ax=ax)
            if zlim:
                ax.set_zlim(zlim)
        
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
        if ax is None:
            plt.show()
        
        
    def plot_lineplot(self, x_data, y_data, x_label='', y_label='', title='', 
                    x_scale='linear', y_scale='linear', xlim=None, ylim=None, 
                    xticks=None, figsize=None, color='k', ax=None):
        if x_data is None or y_data is None:
            raise ValueError('x_data and y_data must be provided')
        
        if figsize is None:
            figsize = self.figsize
        
        if ax is None:
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
        if ax is None:
            plt.show()
        
        
    def Qfactor_lineplot(self, FreqS, QualityFactor, bias_voltages=None, figsize=None, ax=None):
        if figsize is None:
            figsize = self.figsize
        
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
                
        if bias_voltages is None:
            ax.plot(FreqS, QualityFactor[:, self.BVI], 'k', linewidth=self.LW, label='0V')
            title = 'Quality Factor @ 0 Volts'
        else:
            colors = ['k', 'r', 'g', 'b', 'c', 'm']
            for i, (voltage, index) in enumerate(bias_voltages):
                color = colors[i % len(colors)]
                ax.plot(FreqS, QualityFactor[:, index], color, linewidth=self.LW, label=f'{voltage}V')
            title = 'Quality Factor at Various Bias Voltages'
        
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(min(FreqS), self.FM)
        ax.set_ylim(0, np.max(QualityFactor))
        ax.set_xticks([0.1, 1, 5, 10, 20])
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Q Factor')
        ax.set_title(title)
        
        if bias_voltages is not None:
            ax.legend()
        
        if ax is None:
            plt.show()

        
        
    def Qfactor_peak_lineplot(self, FreqS, QFFiltVolt, figsize=None, ax=None):
        if figsize is None:
            figsize = self.figsize
        
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        ax.plot(FreqS, QFFiltVolt, 'k', linewidth=self.LW)
        ax.set_xlim(0.1, self.FM)
        ax.set_ylim(0, self.VoltMax*1.1)
        ax.set_xlabel('Frequency (GHz)')
        ax.set_ylabel('Bias Voltage')
        ax.set_title('Quality Factor Peak at Individual Frequencies')
        
        if ax is None:
            plt.show()
        

        
    # capacitance
    def capacitance_lineplot(self, V, FreqS, Capacitance3D, xaxis='voltage', fit_params=None, figsize=None, ax=None):
        if V is None or FreqS is None or Capacitance3D is None:
            raise ValueError('Voltage, Frequency, and Capacitance data must be provided')
        
        if figsize is None:
            figsize = self.figsize
        
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
                
        if xaxis == 'voltage':
            ax.plot(V, Capacitance3D[self.params['DispIndex'],:], 'k', linewidth=self.LW)
            
            if not isinstance(fit_params, type(None)):
                label = f'Fit: C_max={fit_params["Cmax_fitted"]:.2e}, V_1/2={fit_params["V_half_fitted"]:.2f}, C_f={fit_params["Cf_fitted"]:.2e}'
                ax.plot(fit_params['V_fit'], fit_params['C_fit'], label=label, linewidth=self.LW, linestyle='--')
                ax.legend()

            ax.set_xlim(-self.params['VoltMax'], self.params['VoltMax'])
            ax.set_xlabel('Bias Voltage')
            ax.set_title('Capacitance @1GHz')
            
        elif xaxis == 'field':
            E_Field = (V / self.params['IDC_gap']) / 1000
            ax.plot(E_Field, Capacitance3D[self.params['DispIndex'],:], 'k', linewidth=self.LW)
            
            if not isinstance(fit_params, type(None)):
                E_Field_fit = (fit_params['V_fit'] / self.params['IDC_gap']) / 1000
                label = f'Fit: C_max={fit_params["Cmax_fitted"]:.2e}, V_1/2={fit_params["V_half_fitted"]:.2f}, C_f={fit_params["Cf_fitted"]:.2e}'
                ax.plot(E_Field_fit, fit_params['C_fit'], label=label, linewidth=self.LW, linestyle='--')
                ax.legend()
                
            ax.set_xlim(-(self.params['VoltMax']/self.params['IDC_gap'])/1000, (self.params['VoltMax']/self.params['IDC_gap'])/1000)
            ax.set_xlabel('Field (kV/cm)')
            ax.set_title('Capacitance @1GHz')
            
        elif xaxis == 'frequency':
            ax.plot(FreqS, Capacitance3D[:,self.params['BVI']], 'k', linewidth=self.LW)
            ax.set_xlim(0, max(FreqS))
            ax.set_ylim(0, max(Capacitance3D[:,self.params['BVI']]) * 1.1)
            ax.set_xlabel('Frequency (GHz)')
            ax.set_title('Capacitance @ 0 Bias')
        
        else:
            raise ValueError('Invalid plot type. Choose "voltage", "field", or "frequency".')
        
        ax.set_ylabel('Capacitance (pF)')
        ax.tick_params(axis='both', which='major')
        plt.tight_layout()
        
        if ax is None:
            plt.show()
        
    # def compare_conductance_capacitance(self, FreqS, QualityFactor, Capacitance3D, Y12r, figsize=None):
    #     fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
    #     # Quality Factor plot
    #     axes[0].plot(FreqS, QualityFactor[:, self.BVI], 'k', linewidth=self.LW)
    #     axes[0].set_yscale('log')
    #     axes[0].set_xlabel('Frequency (GHz)')
    #     axes[0].set_ylabel('Q Factor')
    #     axes[0].set_title('Quality Factor @ 0 Bias')

    #     # Capacitance plot
    #     axes[1].plot(FreqS, Capacitance3D[:, self.BVI], 'k', linewidth=self.LW)
    #     axes[1].set_xlim(0, max(FreqS))
    #     axes[1].set_ylim(0, max(Capacitance3D[:, self.BVI])*1.1)
    #     axes[1].set_xlabel('Frequency (GHz)')
    #     axes[1].set_ylabel('Capacitance (pF)')
    #     axes[1].set_title('Capacitance @ 0 Bias')

    #     # Conductance plot
    #     axes[2].plot(FreqS, np.abs(Y12r[:, self.BVI]), 'k', linewidth=self.LW)
    #     axes[2].set_yscale('log')
    #     axes[2].set_xlabel('Frequency (GHz)')
    #     axes[2].set_ylabel('Conductance (Siemens)')
    #     axes[2].set_title('Conductance @ 0 Bias')

    #     plt.suptitle('Conductance and Capacitance Comparison', fontsize=16)
    #     plt.tight_layout()
    #     plt.show()
            
        
            
            
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
            
    def s_parameter_lineplot(self, FreqS, S_data, voltages, title, ylim, ax=None):
        """
        Plots S-parameter (S11 or S21) vs Frequency for various voltages.
        
        :param FreqS: 1D array of frequency values
        :param S_data: 2D array of S-parameter magnitudes (S11 or S21)
        :param voltages: List of voltage indices to plot
        :param s_type: String, either 'S11' or 'S21'
        :param y_min, y_max: Y-axis limits for the plot
        :param ax: Optional matplotlib axis to plot on
        """
        if FreqS is None or S_data is None:
            raise ValueError('Frequency and S-parameter data must be provided')
        
        if title not in ['S11', 'S21']:
            raise ValueError("s_type must be either 'S11' or 'S21'")
        
        colors = plt.get_cmap(self.cmap)(np.linspace(0, 1, len(voltages)))
        
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
        
        handles = []
        for v, c in zip(voltages, colors):
            line, = ax.plot(FreqS, S_data[:, v], c=c, linewidth=self.LW)
            handles.append(line)
        
        ax.set_xlim(0, self.FM)
        ax.set_ylim(*ylim)
        ax.set_xlabel('Frequency (GHz)')
        ax.set_ylabel('Magnitude (dB)')
        ax.set_title(title)
        ax.legend(handles, [f'{v}V' for v in voltages])
        
        if ax is None:
            plt.tight_layout()
            plt.show()
            
    # def s_parameters_lineplot(self, FreqS, S11m, S21m, voltages, S11min, S11max, S21min, S21max):
    #     """
    #     Plots S-parameters (S11 and S21) vs Frequency for various voltages.
        
    #     :param FreqS: 1D array of frequency values
    #     :param S11m: 2D array of S11 magnitudes
    #     :param S21m: 2D array of S21 magnitudes
    #     :param S11min, S11max: Y-axis limits for S11 plot
    #     :param S21min, S21max: Y-axis limits for S21 plot
    #     """
    #     if FreqS is None or S11m is None or S21m is None:
    #         raise ValueError('Frequency and S-parameter data must be provided')

    #     # voltages = [100, 105, 110, 115, 120, 130, 140, 150, 175, 200]
    #     # voltages = [100, 110, 120, 130, 150, 200]
    #     colors = plt.get_cmap(self.cmap)(np.linspace(0, 1, len(voltages)))
        
    #     fig, axes = plt.subplots(1, 2, figsize=(self.figsize[0]*2, self.figsize[1]))
        
    #     handles = []
    #     for v, c in zip(voltages, colors):
    #         line, = axes[0].plot(FreqS, S11m[:, v], c=c, linewidth=self.LW)
    #         handles.append(line)
    #     axes[0].set_xlim(0, self.FM)
    #     axes[0].set_ylim(S11min, S11max)
    #     axes[0].set_xlabel('Frequency (GHz)')
    #     axes[0].set_ylabel('Magnitude (dB)')
    #     axes[0].set_title('S_11')
    #     axes[0].legend(handles, [f'{v}V' for v in voltages])

    #     for v, c in zip(voltages, colors):
    #         axes[1].plot(FreqS, S21m[:, v], c=c, linewidth=self.LW)
    #     axes[1].set_xlim(0, self.FM)
    #     axes[1].set_ylim(S21min, S21max)
    #     axes[1].set_xlabel('Frequency (GHz)')
    #     axes[1].set_ylabel('Magnitude (dB)')
    #     axes[1].set_title('S_21')
    #     axes[1].legend(handles, [f'{v}V' for v in voltages])

    #     plt.tight_layout()
    #     plt.show()   
        
        
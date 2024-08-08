import numpy as np
from scipy import signal
from scipy.optimize import least_squares
import skrf as rf
from tqdm import tqdm

class CapacitorAnalysis:
    def __init__(self, params):
        self.params = params
        if params is None:
            raise ValueError('params is required')
            
    def setup_params(self, files_dict):
        print('Setup parameters:')

        S = [None] * self.params['N']
        for file, k in files_dict.items():
            S[k] = rf.Network(file)
        # self.params['S'] = S

        Freq = S[0].f
        FreqS = Freq / 1e9
        w = 2 * np.pi * Freq

        S11i, S12i, S21i, S22i = [np.zeros((len(Freq), self.params['N'])) for _ in range(4)]
        S11r, S12r, S21r, S22r = [np.zeros((len(Freq), self.params['N'])) for _ in range(4)]
        Y11i, Y12i, Y21i, Y22i = [np.zeros((len(Freq), self.params['N'])) for _ in range(4)]
        Y11r, Y12r, Y21r, Y22r = [np.zeros((len(Freq), self.params['N'])) for _ in range(4)]
        Z11i, Z12i, Z21i, Z22i = [np.zeros((len(Freq), self.params['N'])) for _ in range(4)]
        Z11r, Z12r, Z21r, Z22r = [np.zeros((len(Freq), self.params['N'])) for _ in range(4)]

        for k in tqdm(range(self.params['N'])):
            S11i[:, k], S12i[:, k], S21i[:, k], S22i[:, k] = [S[k].s[:, i, j].imag for i, j in [(0,0), (0,1), (1,0), (1,1)]]
            S11r[:, k], S12r[:, k], S21r[:, k], S22r[:, k] = [S[k].s[:, i, j].real for i, j in [(0,0), (0,1), (1,0), (1,1)]]
            Y11i[:, k], Y12i[:, k], Y21i[:, k], Y22i[:, k] = [S[k].y[:, i, j].imag for i, j in [(0,0), (0,1), (1,0), (1,1)]]
            Y11r[:, k], Y12r[:, k], Y21r[:, k], Y22r[:, k] = [S[k].y[:, i, j].real for i, j in [(0,0), (0,1), (1,0), (1,1)]]
            Z11i[:, k], Z12i[:, k], Z21i[:, k], Z22i[:, k] = [S[k].z[:, i, j].imag for i, j in [(0,0), (0,1), (1,0), (1,1)]]
            Z11r[:, k], Z12r[:, k], Z21r[:, k], Z22r[:, k] = [S[k].z[:, i, j].real for i, j in [(0,0), (0,1), (1,0), (1,1)]]
        
        S11m = 20 * np.log10(np.sqrt(S11r**2 + S11i**2))
        S12m = 20 * np.log10(np.sqrt(S12r**2 + S12i**2))
        S21m = 20 * np.log10(np.sqrt(S21r**2 + S21i**2))
        S22m = 20 * np.log10(np.sqrt(S22r**2 + S22i**2))        
        
        params_calculation = {'Freq': Freq, 'FreqS': FreqS, 'w': w,
                            'S11i': S11i, 'S12i': S12i, 'S21i': S21i, 'S22i': S22i,
                            'S11r': S11r, 'S12r': S12r, 'S21r': S21r, 'S22r': S22r,
                            'Y11i': Y11i, 'Y12i': Y12i, 'Y21i': Y21i, 'Y22i': Y22i,
                            'Y11r': Y11r, 'Y12r': Y12r, 'Y21r': Y21r, 'Y22r': Y22r,
                            'Z11i': Z11i, 'Z12i': Z12i, 'Z21i': Z21i, 'Z22i': Z22i,
                            'Z11r': Z11r, 'Z12r': Z12r, 'Z21r': Z21r, 'Z22r': Z22r,
                            'S11m': S11m, 'S12m': S12m, 'S21m': S21m, 'S22m': S22m,}
        params_calculation.update(self.params)
        self.params = params_calculation
        return params_calculation


    @staticmethod
    def calculate_capacitance(Y12i, w, CF, VoltMid):
        Capacitance3D = np.abs((Y12i / w[:, np.newaxis]) / 1e-12)
        Capacitance3D -= CF
        CapacitanceMin = np.min(Capacitance3D, axis=1)
        Capacitance0Volt = Capacitance3D[:, VoltMid]
        return Capacitance3D, CapacitanceMin, Capacitance0Volt

    @staticmethod
    def calculate_conductance(Y12r, Y11r, w):
        Y12Conductance3D = np.abs((Y12r / w[:, np.newaxis]) / 1e-12)
        Y11Conductance3D = np.abs((Y11r / w[:, np.newaxis]) / 1e-12)
        DiffConductance3D = Y12Conductance3D + Y11Conductance3D
        return Y12Conductance3D, Y11Conductance3D, DiffConductance3D

    @staticmethod
    def calculate_tunability(Capacitance3D, Capacitance0Volt, CapacitanceMin):
        Tunability3D = Capacitance0Volt[:, np.newaxis] / Capacitance3D
        Tunability2D = Capacitance0Volt / CapacitanceMin
        return Tunability3D, Tunability2D

    @staticmethod
    def calculate_quality_factor(Y12i, Y12r):
        return np.abs(Y12i / Y12r)

    @staticmethod
    def calculate_loss_tangent(Y11r, Y11i):
        return np.abs(Y11r / Y11i)

    @staticmethod
    def calculate_commutation_quality_factor(Y12i, Y12r, VoltMid):
        CQF = (np.abs((Y12i[:, VoltMid] - Y12i[:, -1])**2 / (Y12r[:, VoltMid] * Y12r[:, -1])) +
               np.abs((Y12i[:, VoltMid] - Y12i[:, 0])**2 / (Y12r[:, VoltMid] * Y12r[:, 0]))) / 2
        return CQF

    @staticmethod
    def calculate_peak_q_factor(QualityFactor, VoltMid, V, FreqS, VoltStep):
        QualityFactorT = QualityFactor.T
        QFS = QualityFactorT.shape
        QFMF = np.zeros((VoltMid, QFS[1]))

        for Index in range(VoltMid):
            QFMF[Index, :] = QualityFactorT[Index + VoltMid, :]

        Vh = V[VoltMid:QFS[0]]
        VoltQPeak = np.zeros(len(FreqS))
        j, k = np.max(QFMF, axis=0), np.argmax(QFMF, axis=0)

        VoltQPeak = k

        B, A = signal.butter(2, 0.1, 'low')
        QFFilt = signal.filtfilt(B, A, VoltQPeak)
        QFFiltVolt = (QFFilt * VoltStep) - VoltStep
        return QFMF, Vh, QFFiltVolt

    @staticmethod
    def fitting_function(p, V):
        return (p[0] - p[2]) / (2 * np.cosh(2/3 * np.arcsinh(2 * V / p[1])) - 1) + p[2]

    @staticmethod
    def fit_capacitance(Capacitance3D, V, FreqS, DispIndex):
        voltages = V
        popts = []

        for n in range(len(FreqS)):
            Capacitance_at_DispIndex = Capacitance3D[DispIndex, :]
            initial_guess = [4.5e-13, 45, 1e-13]
            
            result = least_squares(lambda p: CapacitorAnalysis.fitting_function(p, voltages) - Capacitance_at_DispIndex, initial_guess)
            popt = result.x
            
            Cmax_fitted, V_half_fitted, Cf_fitted = popt
            V_fit = np.linspace(min(voltages), max(voltages), 1000)
            C_fit = CapacitorAnalysis.fitting_function(popt, V_fit)
            popts.append(popt)
        
        return V_fit, C_fit, Cmax_fitted, V_half_fitted, Cf_fitted

        
    def run_analysis(self):
        print('Calculate:')
        
        # Unpack the necessary parameters
        Y12i, Y12r, Y11i, Y11r, w, FreqS = self.params['Y12i'], self.params['Y12r'], self.params['Y11i'], self.params['Y11r'], self.params['w'], self.params['FreqS']
        
        # Use unpacked parameters in function calls
        Capacitance3D, CapacitanceMin, Capacitance0Volt = self.calculate_capacitance(Y12i, w, self.params['CF'], self.params['VoltMid'])
        Y12Conductance3D, Y11Conductance3D, DiffConductance3D = self.calculate_conductance(Y12r, Y11r, w)
        Tunability3D, Tunability2D = self.calculate_tunability(Capacitance3D, Capacitance0Volt, CapacitanceMin)
        QualityFactor = self.calculate_quality_factor(Y12i, Y12r)
        LossTan = self.calculate_loss_tangent(Y11r, Y11i)
        CQF = self.calculate_commutation_quality_factor(Y12i, Y12r, self.params['VoltMid'])
        QFMF, Vh, QFFiltVolt = self.calculate_peak_q_factor(QualityFactor, self.params['VoltMid'], self.params['V'], FreqS, self.params['VoltStep'])
        V_fit, C_fit, Cmax_fitted, V_half_fitted, Cf_fitted = self.fit_capacitance(Capacitance3D, self.params['V'], FreqS, self.params['DispIndex'])

        return {'Capacitance3D': Capacitance3D,
                'CapacitanceMin': CapacitanceMin,
                'Capacitance0Volt': Capacitance0Volt,
                'Y12Conductance3D': Y12Conductance3D,
                'Y11Conductance3D': Y11Conductance3D,
                'DiffConductance3D': DiffConductance3D,
                'Tunability3D': Tunability3D,
                'Tunability2D': Tunability2D,
                'QualityFactor': QualityFactor,
                'LossTan': LossTan,
                'CQF': CQF,
                'QFMF': QFMF,
                'Vh': Vh,
                'QFFiltVolt': QFFiltVolt,
                'V_fit': V_fit,
                'C_fit': C_fit,
                'Cmax_fitted': Cmax_fitted,
                'V_half_fitted': V_half_fitted,
                'Cf_fitted': Cf_fitted
                }
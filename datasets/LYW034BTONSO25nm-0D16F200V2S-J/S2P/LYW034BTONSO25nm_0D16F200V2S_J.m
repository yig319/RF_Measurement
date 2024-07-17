clear all
clc
close all
%-----------Inputs for each dataset-------------
VoltMax = 200;
VoltStep = 2;


DispIndex = 100; % Frequency index for capacitance graph
BVI = 101; % Bias voltage index for single voltage graph
FM = 26.5; % Max frequency to graph

FT = 32; % Graph Font Size
LW = 6; % Line Width

QFSL = 10; % Q factor plot min
QFSH = 10e3; % Q factor plot max

Cap3DL = 0.05; % 3D Capacitance plot min 
Cap3DH = 0.1; % 3D Capacitance plot max

TunL = 1; % Tunability plot min
TunH = 2; % Tunability plot max

LTmin = 0.01; % Loss Tangent min
LTmax = 0.5; % Loss Tangent max

%Y11rL = ; % Y11 Real plot min
%Y11rH = ; % Y11 Real plot max
%Y111L = ; % Y11 Imaginary plot min
%Y111H = ; % Y11 Imaginary plot max
%Y12rL = ; % Y12 Real plot min
%Y12rH = ; % Y12 Real plot max
%Y12iL = ; % Y12 Imaginary plot min
%Y12iH = ; % Y12 Imaginary plot max

%DifY11rL = ; % Difference in the Y11 conductance plot min 
%DifY11rH = ; % Difference in the Y11 conductance plot max

S11min = -5; % S11 Plot min
S11max = 0; % S11 Plot max
S21min = -30; % S21 Plot min
S21max = 0; % S21 Plot max

IDC_gap = 3e-4; % IDC gap size in mm
CF = 0; % Capacitance correction factor

%------------Variable Definitions----------------
VoltMid = (VoltMax/VoltStep);
V = -VoltMax:VoltStep:VoltMax;
N = numel(V);
S = cell(1,N);
Y = cell(1,N);
Z = cell(1,N);
Eff = (V/IDC_gap)/1000;

%------------Importing S2P Files-----------------
for k = VoltMid+1:N
    File = sprintf('LYW034BTONSO25nm_0D16F200V2S_J_%dV_dev.s2p',V(k)); %Copy file name
    S{k} = sparameters(File);
    Y{k} = yparameters(File);
    Z{k} = zparameters(File);
end
for k = 1:VoltMid
    File = sprintf('LYW034BTONSO25nm_0D16F200V2S_J_N%dV_dev.s2p',V(N+1-k)); %Copy file name
    S{k} = sparameters(File);
    Y{k} = yparameters(File);
    Z{k} = zparameters(File);
end

%------------Variable Definitions----------------
Freq = S{1,1}.Frequencies;
FreqS = Freq/1e9;
w = 2 * pi * Freq;

%------------Creating S,Y,Z Variables------------
for k = 1:N
    S11i(:,k)= imag(rfparam(S{k},1,1));
    S12i(:,k)= imag(rfparam(S{k},1,2));
    S21i(:,k)= imag(rfparam(S{k},2,1));
    S22i(:,k)= imag(rfparam(S{k},2,2));
    S11r(:,k)= real(rfparam(S{k},1,1));
    S12r(:,k)= real(rfparam(S{k},1,2));
    S21r(:,k)= real(rfparam(S{k},2,1));
    S22r(:,k)= real(rfparam(S{k},2,2));
    
    Y11i(:,k)= imag(rfparam(Y{k},1,1));
    Y12i(:,k)= imag(rfparam(Y{k},1,2));
    Y21i(:,k)= imag(rfparam(Y{k},2,1));
    Y22i(:,k)= imag(rfparam(Y{k},2,2));
    Y11r(:,k)= real(rfparam(Y{k},1,1));
    Y12r(:,k)= real(rfparam(Y{k},1,2));
    Y21r(:,k)= real(rfparam(Y{k},2,1));
    Y22r(:,k)= real(rfparam(Y{k},2,2));
    
    Z11i(:,k)= imag(rfparam(Z{k},1,1));
    Z12i(:,k)= imag(rfparam(Z{k},1,2));
    Z21i(:,k)= imag(rfparam(Z{k},2,1));
    Z22i(:,k)= imag(rfparam(Z{k},2,2));
    Z11r(:,k)= real(rfparam(Z{k},1,1));
    Z12r(:,k)= real(rfparam(Z{k},1,2));
    Z21r(:,k)= real(rfparam(Z{k},2,1));
    Z22r(:,k)= real(rfparam(Z{k},2,2));
end

S11m = 20 * log10(sqrt(S11r.^2 + S11i.^2));
S12m = 20 * log10(sqrt(S12r.^2 + S12i.^2));
S21m = 20 * log10(sqrt(S21r.^2 + S21i.^2));
S22m = 20 * log10(sqrt(S22r.^2 + S22i.^2));

%------------Capacitance Calculations------------
for k = 1:N
    Capacitance3D(:,k) = abs((Y12i(:,k)./w)/1e-12);
end

Capacitance3D = Capacitance3D - CF;

for k =1:length(Freq)
    CapacitanceMin(k) = min(Capacitance3D(k,:));
end
Capacitance0Volt = Capacitance3D(:,VoltMid+1);

%------------Conductance Calculations------------
for k = 1:N
    Y12Conductance3D(:,k) = abs((Y12r(:,k)./w)/1e-12);
end

for k = 1:N
    Y11Conductance3D(:,k) = abs((Y11r(:,k)./w)/1e-12);
end

DiffConductance3D = Y12Conductance3D + Y11Conductance3D;

%--------------Tunability Calculations-----------
for k = 1:N
    Tunability3D(:,k) = Capacitance3D(:,VoltMid+1)./Capacitance3D(:,k);
end
for k =1:length(Freq)
    Tunability2D(k) = Capacitance0Volt(k)./CapacitanceMin(k);
end

%----------Quality Factor Calculations-----------
QualityFactor = abs(Y12i./Y12r);

%-----------Loss Tangent Calculations------------
LossTan = abs(Y11r./Y11i);

%-----Commutation Quality Factor Calculations----

ZZ12i = 1./Y12i;
ZZ12r = 1./Y12r;

%CQF = 1./(abs(((ZZ12i(:,VoltMid+1)-ZZ12i(:,N)).^2)./(ZZ12r(:,VoltMid+1).*ZZ12r(:,N))));

CQF = (((abs(((Y12i(:,VoltMid+1)-Y12i(:,N)).^2)./(Y12r(:,VoltMid+1).*Y12r(:,N)))))+((abs(((Y12i(:,VoltMid+1)-Y12i(:,1)).^2)./(Y12r(:,VoltMid+1).*Y12r(:,1))))))./2;

%---------Peak Q Factor at Each Frequency--------
QualityFactorT=QualityFactor';
QFS = size(QualityFactorT);
QFMF = zeros(VoltMid,QFS(2));

for Index = 1:VoltMid+1
    QFMF(Index,:) = QualityFactorT(Index+VoltMid,:);
end

Vh=V(VoltMid+1:QFS(1));
VoltQPeak = zeros(length(FreqS),1);
VoltQPeakCor = zeros(length(FreqS),1);
[j,k] = max(QFMF);

for Index = 1:length(FreqS)
    VoltQPeak(Index) = k(Index);
end

[B,A] = butter(2,0.1,'low');
QFFilt = filtfilt(B,A,VoltQPeak);
QFFiltVolt = (QFFilt * VoltStep)-VoltStep;

%----------------Capacitance Fitting-------------

% Define the fitting function including Cf
fitting_function = @(p, V) (p(1) - p(3)) ./ (2 .* cosh(2/3 .* asinh(2 .* V ./ p(2))) - 1) + p(3);
% Your capacitance data
voltages = V;
popts = [];
for n=1:1:numel(FreqS)
    Capacitance_at_DispIndex = Capacitance3D(DispIndex,:); % Replace with your actual capacitance data array
    % Initial guess for the parameters
    initial_guess = [4.5e-13, 45, 1e-13];
    % Perform the curve fitting
    options = optimset('Display', 'off'); % Option to turn off display
    popt = lsqcurvefit(fitting_function, initial_guess, voltages, Capacitance_at_DispIndex, [], [], options);
    % Extract the fitted parameters
    Cmax_fitted = popt(1);
    V_half_fitted = popt(2);
    Cf_fitted = popt(3);
    % Use the fitted parameters to plot the fitted curve
    V_fit = linspace(min(voltages), max(voltages), 1000); % Fine voltage range for a smooth curve
    C_fit = fitting_function(popt, V_fit);
    popts(n,:) = popt;
end

%------------------Save Variable-----------------
LYW034BTONSO25nm_0D16F200V2S_J_Tunability = Tunability2D;
save('LYW034BTONSO25nm_0D16F200V2S_J_Tunability.mat', 'LYW034BTONSO25nm_0D16F200V2S_J_Tunability')
LYW034BTONSO25nm_0D16F200V2S_J_QFPeakatFreq = QFFiltVolt;
save('LYW034BTONSO25nm_0D16F200V2S_J_QFPeakatFreq.mat', 'LYW034BTONSO25nm_0D16F200V2S_J_QFPeakatFreq')

%----------------Figure Generation---------------
figure('Name','Quality Factor');%------------------------------------------------------Quality Factor
surf(V, FreqS, QualityFactor)
axis([-VoltMax VoltMax 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
caxis([QFSL QFSH])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Q Factor')
title('Quality Factor')

figure('Name','Quality Factor');%-------------------------------------Quality Factor (Electric Field)
surf((V/IDC_gap)/1000, FreqS, QualityFactor)
axis([-(VoltMax/IDC_gap)/1000 (VoltMax/IDC_gap)/1000 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
caxis([QFSL QFSH])
set(gca,'fontsize', FT)
xlabel('Field (kV/cm)')
ylabel('Frequency (GHz)')
zlabel('Q Factor')
title('Quality Factor')

figure('Name','Quality Factor Positive Voltage Bias');%---------------------Quality Factor Positive
surf(FreqS, Vh, QFMF)
axis([0.1 FM 0 VoltMax])
view(90,270)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
caxis([QFSL QFSH])
set(gca,'fontsize', FT)
xlabel('Frequency (GHz)')
ylabel('Bias Voltage')
zlabel('Q Factor')
title('Quality Factor')

figure('Name','Quality Factor 0 Volt Bias');%-----------------Quality Factor at Specific Bias Voltage
plot(FreqS,QualityFactor(:,BVI),'k','LineWidth',LW)
set(gca, 'fontsize', FT)
set(gca, 'fontsize', FT, 'XScale', 'log')
axis([min(FreqS) FM 0 max(QualityFactor,[],'all')])
xtick = [0.1 1 10 20];
xticks(xtick);
set(gca, 'fontsize', FT, 'YScale', 'log')
xlabel('Frequency')
ylabel('Q Factor')
title('Quality Factor @ 0 Volts')

figure('Name','Quality Factor Various Bias');%-----------------Quality Factor at Specific Bias Voltage (Multi Points)
plot(FreqS,QualityFactor(:,BVI),'k','LineWidth',LW)
hold on
plot(FreqS,QualityFactor(:,111),'r','LineWidth',LW)
plot(FreqS,QualityFactor(:,121),'g','LineWidth',LW)
plot(FreqS,QualityFactor(:,141),'b','LineWidth',LW)
plot(FreqS,QualityFactor(:,161),'c','LineWidth',LW)
plot(FreqS,QualityFactor(:,201),'m','LineWidth',LW)
set(gca, 'fontsize', FT)
axis([min(FreqS) FM 0 max(QualityFactor,[],'all')])
xtick = [0.1 1 5 10 20];
xticks(xtick);
set(gca, 'fontsize', FT, 'YScale', 'log')
xlabel('Frequency')
ylabel('Q Factor')
title('Quality Factor at Varous Bias Voltages')
legend('0V','20V','40V','80V','120V','200V')

figure('Name','Q Peak Location');%--------------------------------------------------Q Peak Location
plot(FreqS,QFFiltVolt,'k','LineWidth',LW)
axis([0.1 FM 0 VoltMax*1.1])
set(gca,'fontsize', FT)
xlabel('Frequency (GHz)')
ylabel('Bias Voltage')
title('Quality Factor Peak at Individual Frequencies')

figure('Name','3D Capacitance');%------------------------------------------------------3D Capacitance
surf(V, FreqS, Capacitance3D)
%axis([-VoltMax VoltMax 0.1 FM])
axis([-VoltMax VoltMax 0.1 FM Cap3DL Cap3DH])
view(45,45)
%view(0,90)
shading interp
set(gca,'fontsize', FT)
colormap jet
colorbar
caxis([Cap3DL Cap3DH])
shading interp
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Capacitance (pF)')
title('Capacitance')

figure('Name','2D Capacitance');%------------------------------------------------2D Capacitance at Specific Frequency (Bias Voltage)
plot(V, Capacitance3D(DispIndex,:),'k','LineWidth',LW)
%axis([-VoltMax VoltMax 0 max(Capacitance3D(DispIndex,:))*1.1])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Capacitance (pF)')
title('Capacitance @1GHz')

figure('Name','2D Capacitance');%------------------------------------------------2D Capacitance at Specific Frequency (Electric Field)
plot((V/IDC_gap)/1000, Capacitance3D(DispIndex,:),'k','LineWidth',LW)
%axis([-(VoltMax/IDC_gap)/1000 (VoltMax/IDC_gap)/1000 0 max(Capacitance3D(DispIndex,:))*1.1])
set(gca,'fontsize', FT)
xlabel('Field (kV/cm)')
ylabel('Capacitance (pF)')
title('Capacitance @1GHz')

figure('Name','2D Capacitance')%----------------------------------------------2D Capacitance at Specific Bias Voltage
plot(FreqS, Capacitance3D(:,BVI),'k','LineWidth',LW)
%axis([0 max(FreqS) min(Capacitance3D(:,BVI))/1.01 max(Capacitance3D(:,BVI))*1.1])
axis([0 max(FreqS) 0 max(Capacitance3D(:,BVI))*1.1])
set(gca,'fontsize', FT)
xlabel('Frequency (GHz)')
ylabel('Capacitance (pF)')
title('Capacitance @ 0 Bias')

figure('Name','Fitted Curve for Capacitance');%--------------------------------Capacitance Fitting Plot
plot(voltages, Capacitance_at_DispIndex, 'o', 'DisplayName', 'Data','LineWidth',LW);
hold on;
plot(V_fit, C_fit, '-', 'DisplayName', sprintf('Fit: C_{max}=%.2e, V_{1/2}=%.2f, C_f=%.2e', Cmax_fitted, V_half_fitted, Cf_fitted),'LineWidth',LW);
set(gca,'fontsize', FT)
xlabel('Voltage (V)');
ylabel('Capacitance at 1 GHz (F)');
title('Capacitance vs Voltage at 1 GHz with Fitted Curve');
legend('show', 'Location', 'south');
grid on;
hold off;

figure('Name','Conductance')%-------------------------------------------------2D Conductance at Specific Bias Voltage
plot(FreqS, abs(Y12r(:,BVI)),'k','LineWidth',LW)
%axis([0 max(FreqS) min(abs(Y12r(:,BVI))/1.01) max(abs(Y12r(:,BVI)))*1.1])
%axis([0 max(FreqS) 0 max(abs(Y12r(:,BVI)))*1.1])
axis([0 FM 0 max(abs(Y12r(:,BVI)))*1.1])
%set(gca,'fontsize', FT)
set(gca,'fontsize', FT, 'YScale', 'log')
xlabel('Frequency (GHz)')
ylabel('Conductance (Siemens)')
title('Conductance @ 0 Bias')

figure('Name','Conductance and Capacitance Comparison');%-------------------Comparison of Capacitance and Conductance 
subplot(2,2,[1 3])
plot(FreqS,QualityFactor(:,BVI),'k','LineWidth',LW)
set(gca, 'fontsize', FT)
%set(gca, 'fontsize', FT, 'XScale', 'log')
xtick = [0.1 1 10 20];
xticks(xtick);
set(gca, 'fontsize', FT, 'YScale', 'log')
xlabel('Frequency (GHz)')
ylabel('Q Factor')
subplot(2,2,2)
plot(FreqS, Capacitance3D(:,BVI),'k','LineWidth',LW)
%axis([0 max(FreqS) min(Capacitance3D(:,BVI))/1.01 max(Capacitance3D(:,BVI))*1.1])
axis([0 max(FreqS) 0 max(Capacitance3D(:,BVI))*1.1])
set(gca,'fontsize', FT)
ylabel('Capacitance (pF)')
subplot(2,2,4)
plot(FreqS, abs(Y12r(:,BVI)),'k','LineWidth',LW)
%axis([0 max(FreqS) min(abs(Y12r(:,BVI))/1.01) max(abs(Y12r(:,BVI)))*1.1])
axis([0 max(FreqS) 0 max(abs(Y12r(:,BVI)))*1.1])
%set(gca,'fontsize', FT)
set(gca,'fontsize', FT, 'YScale', 'log')
xlabel('Frequency (GHz)')
ylabel('Conductance (Siemens)')
sgtitle('Conductance and Capacitance Comparison','fontsize', FT) 

figure('Name','3D Tunability');%------------------------------------------------------3D Tunability
surf(V, FreqS, Tunability3D)
axis([-VoltMax VoltMax 0.1 FM TunL TunH])
set(gca,'fontsize', FT)
colormap jet
colorbar
caxis([TunL TunH])
view(45,45)
shading interp
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Tunability')
title('Tunability')

figure('Name','2D Tunability');%--------------------------------------------------------2D Tunability
plot(FreqS,Tunability2D,'k','LineWidth',LW)
axis([0.1 FM TunL TunH])
set(gca, 'fontsize', FT, 'XScale', 'log')
xtick = [0.1 1 10 20];
xticks(xtick);
title('Tunability')
xlabel('Frequency (GHz)')
ylabel('Tunability')

figure('Name','CQF');%----------------------------------------------------------------------------CQF
plot(FreqS,CQF,'k','LineWidth',LW)
axis([0.1 20 min(CQF)/1.1 max(CQF)*1.1])
set(gca, 'fontsize', FT, 'XScale', 'log')
set(gca, 'fontsize', FT, 'YScale', 'log')
xtick = [0.1 1 10 20];
xticks(xtick);
title('CQF')
xlabel('Frequency (GHz)')
ylabel('CQF')

figure('Name','Loss Tangent');%--------------------------------------------------------Loss Tangent
surf(V, FreqS, LossTan)
set(gca,'fontsize', FT)
colormap jet
colorbar
set(gca,'ColorScale','log')
set(gca, 'ZScale','log')
view(0,90)
shading interp
caxis([LTmin LTmax])
axis([-VoltMax VoltMax 0.1 FM])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Loss Tangent')
title('Loss Tangent')

figure('Name','S11 Plots');%-----------------------------------------------------------S Parameters
plot(FreqS,S11m(:,101),'k','LineWidth',LW)
hold on
plot(FreqS,S11m(:,111),'r','LineWidth',LW)
plot(FreqS,S11m(:,126),'b','LineWidth',LW)
plot(FreqS,S11m(:,141),'g','LineWidth',LW)
plot(FreqS,S11m(:,166),'c','LineWidth',LW)
plot(FreqS,S11m(:,201),'m','LineWidth',LW)
axis([0 FM S11min S11max])
xlabel('Frequency (GHz)')
ylabel('Magnitude (dB)')
legend('0V','20V','50V','80V','130V','200V')
title('S_{11}')
set(gca, 'fontsize', FT)

figure('Name','S21 Plots');
plot(FreqS,S21m(:,101),'k','LineWidth',LW)
hold on
plot(FreqS,S21m(:,111),'r','LineWidth',LW)
plot(FreqS,S21m(:,126),'b','LineWidth',LW)
plot(FreqS,S21m(:,141),'g','LineWidth',LW)
plot(FreqS,S21m(:,166),'c','LineWidth',LW)
plot(FreqS,S21m(:,201),'m','LineWidth',LW)
set(gca, 'fontsize', FT)
axis([0 FM S21min S21max])
title('S_{21}')
xlabel('Frequency (GHz)')
ylabel('Magnitude (dB)')
legend('0V','20V','50V','80V','130V','200V')

figure('Name','S11 Plots')
h = rfplot(S{101},1,1);
set(h,'Color', [1 0 0], 'LineWidth', LW);
hold on
h = rfplot(S{106},1,1);
set(h,'Color', [0 1 0], 'LineWidth', LW);
h = rfplot(S{111},1,1);
set(h,'Color', [0 0 1], 'LineWidth', LW);
h = rfplot(S{116},1,1);
set(h,'Color', [1 1 0], 'LineWidth', LW);
h = rfplot(S{121},1,1);
set(h,'Color', [0 1 1], 'LineWidth', LW);
h = rfplot(S{131},1,1);
set(h,'Color', [1 0 1], 'LineWidth', LW);
h = rfplot(S{141},1,1);
set(h,'Color', [0.5 0 0], 'LineWidth', LW);
h = rfplot(S{151},1,1);
set(h,'Color', [0 0.5 0], 'LineWidth', LW);
h = rfplot(S{176},1,1);
set(h,'Color', [0 0 0.5], 'LineWidth', LW);
h = rfplot(S{201},1,1);
set(h,'Color', [0.5 0.5 0], 'LineWidth', LW);
set(gca, 'fontsize', 32)
axis([0 FM S11min S11max])
title('S_{11}')
xlabel('Frequency (GHz)')
ylabel(('S_{11} (dB)'))
legend('0V','10V','20V','30V','40V','60V','80V','100V','150V','200V')

figure('Name','S21 Plots')
h = rfplot(S{101},2,1);
set(h,'Color', [1 0 0], 'LineWidth', LW);
hold on
h = rfplot(S{106},2,1);
set(h,'Color', [0 1 0], 'LineWidth', LW);
h = rfplot(S{111},2,1);
set(h,'Color', [0 0 1], 'LineWidth', LW);
h = rfplot(S{116},2,1);
set(h,'Color', [1 1 0], 'LineWidth', LW);
h = rfplot(S{121},2,1);
set(h,'Color', [0 1 1], 'LineWidth', LW);
h = rfplot(S{131},2,1);
set(h,'Color', [1 0 1], 'LineWidth', LW);
h = rfplot(S{141},2,1);
set(h,'Color', [0.5 0 0], 'LineWidth', LW);
h = rfplot(S{151},2,1);
set(h,'Color', [0 0.5 0], 'LineWidth', LW);
h = rfplot(S{176},2,1);
set(h,'Color', [0 0 0.5], 'LineWidth', LW);
h = rfplot(S{201},2,1);
set(h,'Color', [0.5 0.5 0], 'LineWidth', LW);
set(gca, 'fontsize', 32)
axis([0 FM S21min S21max])
title('S_{21}')
xlabel('Frequency (GHz)')
ylabel(('S_{21} (dB)'))
legend('0V','10V','20V','30V','40V','60V','80V','100V','150V','200V')

figure('Name','Y12 Imaginary');%------------------------------------------------------Y12 Imaginary
surf(V, FreqS, abs(Y12i))
axis([-VoltMax VoltMax 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
%caxis([Y12iL Y12iH])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Reactance')
title('Reactance')

figure('Name','Y12 Real');%----------------------------------------------------------------Y12 Real
surf(V, FreqS, Y12Conductance3D)
axis([-VoltMax VoltMax 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
%caxis([Y12rL Y12rH])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Conductance (Siemens)')
title('Conductance')

figure('Name','Y11 Imaginary');%------------------------------------------------------Y11 Imaginary
surf(V, FreqS, abs(Y11i))
axis([-VoltMax VoltMax 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
%caxis([Y11iL Y11iH])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Reactance')
title('Reactance')

figure('Name','Y11 Real');%----------------------------------------------------------------Y11 Real
surf(V, FreqS, Y11Conductance3D)
axis([-VoltMax VoltMax 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
%caxis([Y11rL Y11rH])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Conductance (Siemens)')
title('Conductance')

figure('Name','Difference in Conduction');%---------------------------------------------Difference in Y11 Conductance
surf(V, FreqS, abs(DiffConductance3D))
axis([-VoltMax VoltMax 0.1 FM])
view(0,90)
shading interp
set(gca,'fontsize', FT)
set(gca,'ColorScale','log')
set(gca,'ZScale','log')
colormap jet
colorbar
%caxis([DifY11rL DifY11rH])
set(gca,'fontsize', FT)
xlabel('Bias Voltage')
ylabel('Frequency (GHz)')
zlabel('Difference in Conductance')
title('Difference in Conductance')
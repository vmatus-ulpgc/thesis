%% PLOT FUCK

%% Clean workspace
close all; clear; clc;

%% Load data and define variables
load video_1.mat

chunk = 150;
offset = 200;

buffer_near = buffer_near(offset:end-5, :);
buffer_far  = buffer_far(offset:end-5, :);

L_near = size(buffer_near, 1);
L_far = size(buffer_far, 1);

%% Process chunks of data
SNR_near = zeros(L_near - chunk, 3);
SNR_far = zeros(L_far - chunk, 3);

background_near = zeros(L_near - chunk, 3);
background_far = zeros(L_far - chunk, 3);


waveform_near = buffer_near(492:492+150, 1);
gmm_near = fitgmdist(waveform_near, 2);


figure('Color','white');
subplot(2,1,1);
x = [0:length(waveform_near)-1]/30;
plot(x, waveform_near, 'k', 'LineWidth', 1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(a)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);
xlabel('Time (s)', 'FontSize', 16, 'interpreter', 'latex');
ylabel('Pixel value','FontSize', 16, 'interpreter', 'latex');

subplot(2,1,2);
[F,x] = ecdf(waveform_near);
plot([0:255], gmm_near.cdf([0:255]'), 'r', 'LineWidth', 1.5);
hold on
plot(x, F, 'k', 'LineWidth', 1.5);
hold off
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(b)', 'FontSize',16, 'interpreter','latex');
xlim([0 255]);
xlabel('Pixel value', 'FontSize', 16, 'interpreter', 'latex');
ylabel('$cdf(x)$','FontSize', 16, 'interpreter', 'latex');

set(gcf, 'PaperPosition',[0 0 20 20], 'PaperSize', [20 20]);
print('gmm','-dpdf');


%% LAST PLOT
figure('Color','white');
T1 = 100;
T2 = 2000;
x = (T1:T2)/30;

waveform_near = buffer_near(T1:T2, 1);
waveform_far = buffer_far(T1:T2, 1);

plot(x, waveform_near, 'k', 'LineWidth', 1.5);
hold on
plot(x, waveform_far, 'r', 'LineWidth', 1.5);
hold off
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
% title('(a)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);
xlabel('Time (s)', 'FontSize', 16, 'interpreter', 'latex');
ylabel('Pixel value','FontSize', 16, 'interpreter', 'latex');
legend('90 m','130 m', 'FontSize', 16, 'interpreter', 'latex');

set(gcf, 'PaperPosition',[0 0 20 20], 'PaperSize', [20 20]);
print('waveform_example','-dpdf');
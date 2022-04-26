
clear; close all; clc;

load video_psf_1.mat

offset = 200;

trunk_far = trunk_far(2:end-3,3:end-2,offset:end-30);
trunk_near = trunk_near(3:end-2,3:end-2,offset:end-30);

% trunk_far = trunk_far - trunk_far(1,1,:);
% trunk_near= trunk_near - trunk_near(1,1,:);

% power_near = zeros(11,11, 2000);
% power_far = zeros(11,11, 2000);


power_near = var(trunk_near(:,:,1000:1250), [], 3);
power_far = var(trunk_far(:,:,1000:1250), [], 3);


[row_near, col_near] = find(power_near == max(power_near,[],'all'));
[row_far, col_far] = find(power_far == max(power_far,[],'all'));

ref_near = squeeze(trunk_near(row_near, col_near, :));
ref_far = squeeze(trunk_far(row_far, col_far, :));

corrs_near = zeros(7,7);
corrs_far = zeros(7,7);

for counter = 1:size(ref_far,1)-501
    for r = 1:7
        for c = 1:7
            aux =  corrcoef(ref_near(1000:1500), trunk_near(r,c,1000:1500));
            corrs_near(r,c) = corrs_near(r,c) + aux(1,2);
            
            aux =  corrcoef(ref_far(1000:1500), trunk_far(r,c,1000:1500));
            corrs_far(r,c) =  corrs_far(r,c)+aux(1,2);
        end
    end
end

corrs_far = corrs_far/counter;
corrs_near = corrs_near/counter;


% [F,x] = ecdf(corrs_near(:));
% th = interp1(F,x,0.75);
% corrs_near(corrs_near < th) = 0;
% 
% 
% [F,x] = ecdf(corrs_far(:));
% th = interp1(F,x,0.75);
% corrs_far(corrs_far < th) = 0;
% % corrs_far(3:5, 3:4) = corrs_far(2:4, 3:4);
% % corrs_far(2,:) = 0;

figure('Color','white');
imagesc(corrs_near);
colormap gray
c = colorbar;
ylabel('pixels', 'FontSize', 16, 'interpreter', 'latex');
xlabel('pixels', 'FontSize', 16, 'interpreter', 'latex');
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
set(c,'FontSize',16, 'TickLabelInterpreter','latex');
set(gcf, 'PaperPosition',[0 0 8 8], 'PaperSize', [8 8]);
title('(a)', 'FontSize',16, 'interpreter','latex');
print('PSF_near','-dpdf');


figure('Color','white');
imagesc(corrs_far);
colormap gray
c = colorbar;
ylabel('pixels', 'FontSize', 16, 'interpreter', 'latex');
xlabel('pixels', 'FontSize', 16, 'interpreter', 'latex');
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
set(c,'FontSize',16, 'TickLabelInterpreter','latex');
set(gcf, 'PaperPosition',[0 0 8 8], 'PaperSize', [8 8]);
title('(b)', 'FontSize',16, 'interpreter','latex');
print('PSF_far','-dpdf');

% NEAR
figure('Color','white');
x = (1200:1400)/30;

subplot(3,1,1)
plot(x,squeeze(trunk_near(4,4,1200:1400)),'k','LineWidth',1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(a)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);

subplot(3,1,2)
plot(x,squeeze(trunk_near(4,5,1200:1400)),'k','LineWidth',1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(b)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);
ylabel('Pixel value', 'FontSize', 16, 'interpreter', 'latex');

subplot(3,1,3)
plot(x,squeeze(trunk_near(4,6,1200:1400)),'k','LineWidth',1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(c)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);
xlabel('Time (s)', 'FontSize', 16, 'interpreter', 'latex');

set(gcf, 'PaperPosition',[0 0 20 20], 'PaperSize', [20 20]);
print('waveform_near','-dpdf');

% FAR
figure('Color','white');
x = (1200:1400)/30;

subplot(3,1,1)
plot(x,squeeze(trunk_far(4,4,1200:1400)),'k','LineWidth',1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(a)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);

subplot(3,1,2)
plot(x,squeeze(trunk_far(4,5,1200:1400)),'k','LineWidth',1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(b)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);
ylabel('Pixel value', 'FontSize', 16, 'interpreter', 'latex');

subplot(3,1,3)
plot(x,squeeze(trunk_far(4,6,1200:1400)),'k','LineWidth',1.5);
set(gca,'FontSize',16, 'TickLabelInterpreter','latex');
title('(c)', 'FontSize',16, 'interpreter','latex');
xlim([x(1) x(end)]);
ylim([0 255]);
xlabel('Time (s)', 'FontSize', 16, 'interpreter', 'latex');

set(gcf, 'PaperPosition',[0 0 20 20], 'PaperSize', [20 20]);
print('waveform_far','-dpdf');
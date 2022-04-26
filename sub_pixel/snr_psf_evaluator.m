%% SNR evaluator
% This script evalutes the SNR

%% Clean workspace
close all; clear; clc;

%% Load data and define variables
load video_psf_full_1.mat
load FILTERS.mat

chunk = 150;

offset = 200;

buffer_far = trunk_far(2:end-3,3:end-2,:,offset:end-30);
buffer_near = trunk_near(3:end-2,3:end-2,:,offset:end-30);

L_near = size(buffer_near, 4);
L_far = size(buffer_far, 4);

buffer_far = squeeze(sum(buffer_far(3:5,3:5, :, :), [1 2]))/9;
buffer_near = squeeze(sum(buffer_near(3:5,3:5, :, :), [1 2]))/9;

% buffer_far = squeeze(sum(buffer_far(3:5,3:5, :, :).*repmat(FILTER_FAR,1,1,3,size(buffer_far,4)), [1 2]))/sum(FILTER_FAR, 'all');
% buffer_near = squeeze(sum(buffer_near(3:5,3:5, :, :).*repmat(FILTER_FAR,1,1,3,size(buffer_far,4)), [1 2]))/sum(FILTER_FAR, 'all');

save signal_averaged.mat buffer_far buffer_near

%% Process chunks of data
SNR_near = zeros(L_near - chunk, 3);
SNR_far = zeros(L_far - chunk, 3);

background_near = zeros(L_near - chunk, 3);
background_far = zeros(L_far - chunk, 3);

for index = 1:min([L_near L_far]) - chunk
    pos = index;
    
    for K = 1:3
        waveform_near = squeeze(buffer_near(K, pos:pos+chunk-1));
        waveform_far =  squeeze(buffer_far(K, pos:pos+chunk-1));
        
        %GMM NEAR
        try
            gmm_near = fitgmdist(waveform_near', 2);
            
            mu_near = gmm_near.mu;
            background_near(index, K) = min(mu_near);
            sigma_near = squeeze(gmm_near.Sigma);
            props_near = gmm_near.ComponentProportion;
           
            
            if (max(props_near) > 0.7)
                SNR_near(index, K) = -Inf;
            else
                
                mu_th = sum(mu_near)/2;
                
                unos = waveform_near(waveform_near > mu_th);
                ceros = waveform_near(waveform_near <= mu_th);
                V1 = 0;
                V2 = 0;
                
                if ~isempty(unos)
                    V1 = var(unos);
                end
                
                if ~isempty(ceros)
                    V2 = var(ceros);
                end
                
                SNR_near(index, K) = 10*log10(0.5*(abs(diff(mu_near)).^2)/(props_near*[V2 V1]'));
            end
            
        catch
            
%             plot(waveform_near);
%             pause;
            SNR_near(index, K) = -Inf;
        end
        
        
        % GMM FAR
        try
            gmm_far = fitgmdist(waveform_far', 2);
            
            mu_far = gmm_far.mu;
            background_far(index, K) = min(mu_far);
            sigma_far = squeeze(gmm_far.Sigma);
            props_far = gmm_far.ComponentProportion;
            
            if (max(props_far) > 0.7)
                SNR_far(index, K) = -Inf;
            else
                
                mu_th = sum(mu_far)/2;
                
                unos = waveform_far(waveform_far > mu_th);
                ceros = waveform_far(waveform_far <= mu_th);
                V1 = 0;
                V2 = 0;
                
                if ~isempty(unos)
                    V1 = var(unos);
                end
                
                if ~isempty(ceros)
                    V2 = var(ceros);
                end
                
                SNR_far(index, K) = 10*log10(0.5*(abs(diff(mu_far)).^2)/(props_far*[V2 V1]'));
            end
        catch
            
%             plot(waveform_far);
%             pause;
            
            SNR_far(index, K) = -Inf;
        end
        
        %       subplot(2,1,1);
        %       plot(0:256, gmm.pdf([0:256]'))
        %       ylim([0 0.2]);
        %       subplot(2,1,2);
        %       plot(waveform);
        %       pause;
    end
    
end

SNR_near = SNR_near(1:index,:);
SNR_far = SNR_far(1:index,:);

SNRrn = mean(SNR_near(~isinf(SNR_near(:,1)),1));
SNRgn = mean(SNR_near(~isinf(SNR_near(:,2)),2));
SNRbn = mean(SNR_near(~isinf(SNR_near(:,3)),3));

SNRrf = mean(SNR_far(~isinf(SNR_far(:,1)),1));
SNRgf = mean(SNR_far(~isinf(SNR_far(:,2)),2));
SNRbf = mean(SNR_far(~isinf(SNR_far(:,3)),3));

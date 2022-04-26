%% SNR evaluator
% This script evalutes the SNR

%% Clean workspace
close; clear; clc;

%% Load data and define variables
load TF.mat

chunk = 150;
offset = 200;

buffer_near = TF(offset:end-5);

L_near = size(buffer_near, 1);

%% Process chunks of data
SNR_near = zeros(L_near - chunk, 1);

background_near = zeros(L_near - chunk, 1);

for index = 1:min([L_near Inf]) - chunk
    pos = index;
    
    for K = 1:1
        waveform_near = squeeze(buffer_near(pos:pos+chunk-1, K));
        
        %GMM NEAR
        try
            gmm_near = fitgmdist(waveform_near, 2);
            
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
            diff
            SNR_near(index, K) = -Inf;
        end
        
    end
end

SNR_near = SNR_near(1:index);

SNRrn = mean(SNR_near(~isinf(SNR_near(:,1))))

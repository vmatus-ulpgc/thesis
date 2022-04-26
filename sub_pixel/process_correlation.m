%% PROCESSING SCRIPT

close all; clear; clc;

load signal_weighed.mat

%% INITIALIZATION
MAT = generate_matrix();

% Timing
frames_per_bit = 4;
frame_length = 15;
delta = 5;

buffer_length = frames_per_bit*frame_length;

% Buffer control
buffer_ptr = 1;

% Duration and offset
offset = 200;
% duration = 3000;

buffer_far = buffer_far';
buffer_near = buffer_near';

buffer_far = buffer_far(offset:end, :);
buffer_near = buffer_near(offset:end, :);

% WITH MA

% buffer = buffer - filter(ones(1,10)/10, 1, buffer);

% Correlation results
corr_results_near = zeros(256, 3, size(buffer_near, 1));
corr_results_far = zeros(256, 3, size(buffer_far, 1));

%% CORRELATION PROCESSING
for pos = 1:size(buffer_far,1)-buffer_length
    slice_far = buffer_far(pos:pos + buffer_length - 1, :);
    slice_near = buffer_near(pos:pos + buffer_length - 1, :);
    
    for K = 1:3
        slice_far(:,K) = (slice_far(:, K) - mean(slice_far(:, K)))/std(slice_far(:, K));
        slice_near(:,K) = (slice_near(:, K) - mean(slice_near(:, K)))/std(slice_near(:, K));
    end
    
    corr_results_far(:, :, pos) =  MAT*slice_far/buffer_length;
    corr_results_near(:, :, pos) =  MAT*slice_near/buffer_length;
    
    if ~mod(pos, 100)
        fprintf('Pos %d/%d\n', pos, size(buffer_near, 1));
    end
    
end


% MEAN CORRELATIONS PER COLOR
[max_corr_near, index_near] = max(corr_results_near,[], 1);
max_corr_near = squeeze(max_corr_near);
index_near = squeeze(index_near);

[max_corr_far, index_far] = max(corr_results_far,[], 1);
max_corr_far = squeeze(max_corr_far);
index_far = squeeze(index_far);

subplot(2,1,1);
plot(max_corr_far(1,:));
title('Far');
subplot(2,1,2);
plot(max_corr_near(1,:));
title('Near');
pause


for K = 1:3
    
    ref_pos_far = 58;
    ref_pos_near = 10;
    step = 60;
    
    slice_width = 5;
    
    final_data_near = [];
    final_data_far = [];
    
    for pos_index = 1:52
        
        if (ref_pos_far <= slice_width)
            slice = max_corr_far(K, 1:ref_pos_far+slice_width);
            indices = index_far(K, 1:ref_pos_far+slice_width);
            [~, I] = max(slice);
            final_data_far(K, end+1) = indices(I);
            ref_pos_far = ref_pos_far + I + step;
        else
            slice = max_corr_far(K, ref_pos_far-slice_width:ref_pos_far+slice_width);
            indices = index_far(K, ref_pos_far-slice_width:ref_pos_far+slice_width);
            [~, I] = max(slice);
            final_data_far(K, end+1) = indices(I);
            ref_pos_far = ref_pos_far - slice_width + I + step;
        end
        
        
        if (ref_pos_near <= slice_width)
            slice = max_corr_near(K, 1:ref_pos_near+slice_width);
            indices = index_near(K, 1:ref_pos_near+slice_width);
            [~, I] = max(slice);
            final_data_near(K, end+1) = indices(I);
            ref_pos_near = ref_pos_near + I + step;
        else
            slice = max_corr_near(K, ref_pos_near-slice_width:ref_pos_near+slice_width);
            indices = index_near(K, ref_pos_near-slice_width:ref_pos_near+slice_width);
            [~, I] = max(slice);
            final_data_near(K, end+1) = indices(I);
            ref_pos_near = ref_pos_near - slice_width + I + step;
        end
        
        
    end
    
    figure
    subplot(2,1,1);
    scatter(1:size(final_data_far,2), final_data_far(K,:));
    title('Far');
    subplot(2,1,2);
    scatter(1:size(final_data_near,2), final_data_near(K,:));
    title('Near');
    
    errors = xor(de2bi(final_data_far(K,:),8), de2bi(mod(127 + (0:size(final_data_far,2)-1), 256), 8));
    BER_far = sum(errors, 'all')/numel(errors)
    
    errors = xor(de2bi(final_data_near(K,:),8), de2bi(mod(55 + (0:size(final_data_near,2)-1), 256), 8));
    BER_near = sum(errors, 'all')/numel(errors)
    
end

%% PROCESSING SCRIPT

%% INITIALIZATION
MAT = generate_matrix();
vid = VideoReader('Manual_captures/pimrc_ss155.mp4');

% Video pixel
row = 613;
col = 727;

% Timing
frames_per_bit = 4;
frame_length = 15;
delta = 5;

buffer_length = frames_per_bit*frame_length;

% Buffer control
buffer = zeros(buffer_length, 3);
buffer_ptr = 1;

while (hasFrame(vid))
   
    % Fetch frame
    frame = readFrame(vid);
    if (buffer_ptr < buffer_length) % Buffer is not full yet
        % Insert in buffer
        buffer(buffer_ptr, :) = frame(row,col,:);
        buffer_ptr = buffer_ptr + 1;
        
        fprintf('Filling buffer %d/%d\n', buffer_ptr, buffer_length);
    else
        % Shift and insert
        buffer(2:buffer_length,:) = buffer(1:buffer_length-1, :);
        buffer(1,:) = frame(row, col, :);
        
        fprintf('New frame inserted\n');
        
        % Now we carry out the fucking correlation
        slice = buffer;
        
        for K = 1:3
            slice(:,K) = (slice(:, K) - mean(slice(:, K)))/std(slice(:, K));
        end
        
        correlations = MAT*slice/frame_length/frames_per_bit;
        
        
        
        max_corr = find(correlations(:,1) > 0.9, 1);
        sync = ~isempty(max_corr);
        soft_bits = slice > 0;
        

        if (sync)
           symbol = max(sort(max_corr));
           fprintf('Found sync at time %1.2f with correlation %1.2f\n', vid.CurrentTime, max(max(correlations)));
           fprintf('Symbol: %d\n\n', symbol);
           subplot(3,1,1);
           plot(buffer(1:frame_length*frames_per_bit));
           subplot(3,1,2);
           stem(soft_bits);
           title(sprintf('Data: %d', symbol));
           
           subplot(3,1,3);
           plot(correlations(:,1));
           pause;
        end
        
    end
    
end
%%% VIEW SIGNAL
%% PROCESSING SCRIPT

%% INITIALIZATION
MAT = generate_matrix();

video_routes = {'VIDEOS/onepix12nov_85us_ag0_dg0.mp4', ...
    'VIDEOS/onepix12nov_15us_ag0_dg0.mp4', ...
    'VIDEOS/onepix12nov_5us_ag0_dg0.mp4'};

video_routes = {'Manual_captures/pimrc_ss155.mp4'};

video_index = 1;

ROW_near = [673 ,673, 673];
COL_near = [818, 818, 818];

ROW_far = [624 ,624, 624];
COL_far = [896, 896, 896];

for route = video_routes
    
    fprintf('Video: %s\n', route{1});
    fprintf('-----------------------\n');
    
    vid = VideoReader(route{1});
    
    % Video pixel
    row_near = ROW_near(video_index); %673;
    col_near = COL_near(video_index); %818;
    row_far = ROW_far(video_index); %673;
    col_far = COL_far(video_index); %818;
    
    % Timing
    frames_per_bit = 4;
    frame_length = 15;
    delta = 5;
    
    buffer_near = zeros(ceil(vid.Duration*vid.FrameRate), 3);
    buffer_far = zeros(ceil(vid.Duration*vid.FrameRate), 3);
    buffer_ptr = 1;    
    
    buffer_near = zeros(500, 3);
    buffer_far = zeros(500, 3);
    buffer_ptr = 1;
    
    
    while (hasFrame(vid))
        
        % Fetch frame
        frame = readFrame(vid);
        buffer_near(buffer_ptr, :) = frame(row_near, col_near, :);
        buffer_far(buffer_ptr, :) = frame(row_far, col_far, :);
        buffer_ptr = buffer_ptr + 1;
        
        if ~mod(buffer_ptr, 100)
            fprintf('Frame %d/%d\n',buffer_ptr, size(buffer_near,1));
        end
        
    end
    
    buffer_near = buffer_near(1:buffer_ptr, :);
    buffer_far = buffer_far(1:buffer_ptr, :);
    
    save(sprintf('video_%d.mat', video_index), 'buffer_near', 'buffer_far');

    video_index = video_index + 1;
    
    delete(vid);
end


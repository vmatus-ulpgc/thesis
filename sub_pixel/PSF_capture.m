%%% VIEW SIGNAL
%% PROCESSING SCRIPT

%% INITIALIZATION

video_routes = {'VIDEOS/onepix12nov_85us_ag0_dg0.mp4', ...
    'VIDEOS/onepix12nov_15us_ag0_dg0.mp4', ...
    'VIDEOS/onepix12nov_5us_ag0_dg0.mp4'};

video_index = 1;

ROW_near = [673 ,673, 673];
COL_near = [818, 818, 818];

ROW_far = [624 ,624, 624];
COL_far = [896, 896, 896];

dev = 5;


for route = video_routes
    
    fprintf('Video: %s\n', route{1});
    fprintf('-----------------------\n');
    
    vid = VideoReader(route{1});
    
    % Video pixel
    row_near = ROW_near(video_index); %673;
    col_near = COL_near(video_index); %818;
    row_far = ROW_far(video_index); %673;
    col_far = COL_far(video_index); %818;
    
    rows_near = row_near-dev:row_near+dev;
    rows_far = row_far-dev:row_far+dev;
    cols_near = col_near-dev:col_near+dev;
    cols_far = col_far-dev:col_far+dev;


    trunk_near = zeros(2*dev+1, 2*dev+1, 3, ceil(vid.Duration*vid.FrameRate));
    trunk_far = zeros(2*dev+1, 2*dev+1, 3, ceil(vid.Duration*vid.FrameRate));
    
    buffer_ptr = 1;
    
    while (hasFrame(vid))
        
        % Fetch frame
        frame = readFrame(vid);
        trunk_near(:,:,:,buffer_ptr) = frame(rows_near, cols_near, :);
        trunk_far(:,:,:,buffer_ptr) = frame(rows_far, cols_far, :);
        buffer_ptr = buffer_ptr + 1;
        
        if ~mod(buffer_ptr, 100)
            fprintf('Frame %d/%d\n',buffer_ptr, size(trunk_near,4));
        end
        
    end
    
    trunk_near = trunk_near(:,:,:,1:buffer_ptr);
    trunk_far = trunk_far(:,:,:,1:buffer_ptr);
    
    save(sprintf('video_psf_full_%d.mat', video_index), 'trunk_near', 'trunk_far');

    video_index = video_index + 1;
    
    delete(vid);
end


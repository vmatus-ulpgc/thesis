video_route = 'VIDEOS/20201218_alineamiento2.mp4';

vid = VideoReader(video_route);

ROW = 531;
COL = 924;

window_size = 150;
fps = 30;

sliding_window_near = zeros(121,window_size);

% vid_near = VideoWriter('focka.mp4');

open(vid_near);

vid.CurrentTime = 4;

counter = 0;

buffer = zeros(101, 101, 60);

corr_pattern = [ones(1,20), -ones(1,4), zeros(1,4*4), -ones(1,4), zeros(1,4*4)];


while(hasFrame(vid))
    frame = double(readFrame(vid))/255;
    
    buffer(:,:,1:end-1) = buffer(:,:,2:end);
    buffer(:,:,end)=squeeze(frame(ROW-50:ROW+50,COL-50:COL+50,1));
    
    if (counter < 60)
        counter = counter + 1;
        fprintf('Populating\n');
        continue;
    end
    
    acc = zeros(size(buffer(:,:,1),1), size(buffer(:,:,1),2));
    
    for I = 1:size(acc,1)
        for J = 1:size(acc,2)
            aux = corrcoef(squeeze(buffer(I,J,:)), corr_pattern);
            acc(I,J) = aux(1,2);
        end
    end
    
    
%     acc = acc/length(corr_pattern) - mean(corr_pattern)*mean(buffer,3);
%     acc = acc/std(corr_pattern)/std(buffer,[],3);
    
%     [r,c] = find(acc > 0.85);
    
    subplot(1,2,1);
    imshow(buffer(:,:,end));
    subplot(1,2,2);
    imagesc(acc);
    colorbar
    title(sprintf('%d', counter));
%     hold on
%     if ~isempty(r)
%         scatter(r,c,'r');
%     end
%     hold off
    
    pause(0.1);
    
    counter = counter + 1;
end

% close(vid_near);
% close(vid_far);
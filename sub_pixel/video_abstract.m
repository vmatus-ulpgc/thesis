video_route = 'VIDEOS/20201218_alineamiento2.mp4';

vid = VideoReader(video_route);

ROW_near = 673;
COL_near = 818;

ROW_far = 624;
COL_far = 896;

window_size = 150;
fps = 30;

sliding_window_near = zeros(1,window_size);
sliding_window_far = zeros(1,window_size);

vid_near = VideoWriter('focka.mp4');
vid_far = VideoWriter('focka2.mp4');

open(vid_near);
open(vid_far);

vid.CurrentTime = 4;

counter = 0;

while(hasFrame(vid))
    frame = readFrame(vid);
    
    if (counter == 0)
       imshow(frame,[]);
       pause;
    end
    
    sample_near = frame(ROW_near+(-3:3), COL_near+(-3:3), :);
    sample_far = frame(ROW_far+(-3:3), COL_far+(-3:3), :);
    
    
    figure(1);
    set(gcf, 'Color', 'white');
    imagesc(sample_near);
    xlabel('Pixel', 'Interpreter', 'Latex', 'FontSize', 16);
    ylabel('Pixel', 'Interpreter', 'Latex', 'FontSize', 16);

    set(gca, 'FontSize', 16, 'TickLabelInterpreter', 'Latex', ...
        'LineWidth',2.0);
    writeVideo(vid_near, getframe(gcf));
    
    
    figure(2);
    set(gcf, 'Color', 'white');
    imagesc(sample_far);
    xlabel('Pixel', 'Interpreter', 'Latex', 'FontSize', 16);
    ylabel('Pixel', 'Interpreter', 'Latex', 'FontSize', 16);
    
    set(gca, 'FontSize', 16, 'TickLabelInterpreter', 'Latex', ...
        'LineWidth',2.0);
    writeVideo(vid_far, getframe(gcf));
    
    counter = counter + 1;
    
    if (mod(counter, 100) == 0)
       fprintf('Frame %d/%d (approx)\n', counter, 3600);
       pause(1);
    end
end


% while(hasFrame(vid))
%     frame = readFrame(vid);
%     sample_near = frame(ROW_near, COL_near, 1);
%     sample_far = frame(ROW_far, COL_far, 1);
%     
%     sliding_window_near = [sliding_window_near(2:end) sample_near];
%     sliding_window_far = [sliding_window_far(2:end) sample_far];
%     
%     time_reference = [counter:counter+window_size-1]/fps;
%     
%     figure(1);
%     set(gcf, 'Color', 'white');
%     plot(time_reference, sliding_window_near,'k','LineWidth',1.5);
%     xlabel('Time (s)', 'Interpreter', 'Latex', 'FontSize', 16);
%     ylabel('Pixel value', 'Interpreter', 'Latex', 'FontSize', 16);
%     ylim([0, 255]);
%     xlim(time_reference([1 end]));
%     set(gca, 'FontSize', 16, 'TickLabelInterpreter', 'Latex', ...
%         'LineWidth',2.0);
%     writeVideo(vid_near, getframe(gcf));
%     
%     
%     figure(2);
%     set(gcf, 'Color', 'white');
%     plot(time_reference, sliding_window_far,'k','LineWidth',1.5);
%     xlabel('Time (s)', 'Interpreter', 'Latex', 'FontSize', 16);
%     ylabel('Pixel value', 'Interpreter', 'Latex', 'FontSize', 16);
%     ylim([0, 255]);
%     xlim(time_reference([1 end]));
%     set(gca, 'FontSize', 16, 'TickLabelInterpreter', 'Latex', ...
%         'LineWidth',2.0);
%     writeVideo(vid_far, getframe(gcf));
%     
%     counter = counter + 1;
%     
%     if (mod(counter, 100) == 0)
%        fprintf('Frame %d/%d (approx)\n', counter, 3600); 
%     end
% end
% 
% close(vid_near);
% close(vid_far);
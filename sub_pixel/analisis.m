%% One pixel
%Authors: Victor Guerra, Vicente Matus
clear all;
close all; 

full_frame = false;

if full_frame
    vid = VideoReader('Manual_captures/pimrc_ss155.mp4');
else
    vid = VideoReader('Manual_captures/1615690958_16_120.mp4'); %1615159356_16_150
%     vid = VideoReader('Manual_captures/1615159356_16_150.mp4'); %1615616426_1_150
%     vid = VideoReader('Manual_captures/1615616426_1_150.mp4'); %1615616426_1_150
    
end

signal = [];
square = [];
noise = [];


% while hasFrame(vid)
if true
    for discard = 1:33
        frame = readFrame(vid);
    end
end

for I = 1:141-discard
    frame = readFrame(vid);
    if full_frame
        frame = frame(590:650, 700:760, :);
%         signal(:,:,end+1) = frame(27-3:27+3, 30-3:30+3);
        signal(:,:,end+1) = frame(27,28);
        square(:,:,end+1) = frame(32, 37);
    else
        frame = frame(110:160, 52:102, :); %vertical, horizontal
%         signal(:,:,end+1) = frame(27-3:27+3, 25-3:25+3);
%         square(:,:,end+1) = frame(30-3:30+3, 29-3:29+3);
        signal(:,:,end+1) = frame(27, 25);
        square(:,:,end+1) = frame(30, 29);
    end
    
%     frame = frame(550:750, 750:950, :);
%     frame = rgb2gray(frame);
%     noise(end+1) = frame(1, 10);
    
    
    imagesc(frame);
    colormap gray
    pause(0.1);

%     if mod(I,100) == 0
%        fprintf('%d/3000\n',I); 
%     end
%     input('ok')
end

% figure();
% signal = signal(1:end);
% square = square(1:end);
% noise = noise(1:end);

% hold on
figure;
subplot(2,1,1);

% plot(signal(4,4,:));
signal = reshape(signal,1,[]);
plot(signal);


subplot(2,1,2);
% plot(square(4,4,:));
square = reshape(square,1,[]);
plot(square);


% for I = 1:7
%     for J = 1:7
%         KAKA(I,J) = mean(signal(I,J,200:end));
%     end
% end

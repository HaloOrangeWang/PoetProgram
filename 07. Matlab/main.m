clear;

settings_2;
videoobj = VideoReader(videopath);
for t = 1: floor(start_sec * fps)
    readFrame(videoobj);
end

frame_data = cell(0);
for t = floor(start_sec * fps) + 1: floor(end_sec * fps)
    frame_data{t - floor(start_sec * fps)} = readFrame(videoobj);
end

new_frame_data = cell(1, length(frame_data));
for frame = 1: length(frame_data)
    fprintf('frame = %d\n', frame);
    frame_data_2 = rgb2gray(frame_data{frame});
    data_1frame = uint8(zeros(720, 1280, 3) + 255);
    for row = 1:720
        for col = 1:1280
            is_border = 0;
            if row >= 2
                if abs(frame_data_2(row, col) - frame_data_2(row - 1, col)) >= 32
                    is_border = 1;
                end
            end
            if row <= 719
                if abs(frame_data_2(row, col) - frame_data_2(row + 1, col)) >= 32
                    is_border = 1;
                end
            end
            if col >= 2
                if abs(frame_data_2(row, col) - frame_data_2(row, col - 1)) >= 32
                    is_border = 1;
                end
            end
            if col <= 1279
                if abs(frame_data_2(row, col) - frame_data_2(row, col + 1)) >= 32
                    is_border = 1;
                end
            end
            if is_border == 1
                data_1frame(row, col, :) = [0, 0, 255];
            end
        end
    end
    new_frame_data{1, frame} = data_1frame;
end

for frame = 1: length(frame_data)
    set(gcf,'Position',[100,50,1280,720]);
    image(new_frame_data{1, frame});
    pause(0.4);
end
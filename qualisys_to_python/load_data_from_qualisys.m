qualisys_file_name = '2022-08-29_Pilot_Data0002.mat'; %Qualisys mat file name 

%% 
filepath = fullfile([pwd,filesep,qualisys_file_name]);

data = load(filepath);

qtm_struct_name = fieldnames(data);

labeled_marker_data = data.(qtm_struct_name{1}).Trajectories.Labeled.Data; 

shape_marker_data = size(labeled_marker_data);

%%

num_markers = shape_marker_data(1);
num_coordinates = 3;
num_frames = shape_marker_data(3);

data_reshaped = nan(num_frames, num_markers, 3);

for frame = 1:num_frames
    for marker = 1:num_markers
        for coordinate = 1:num_coordinates
    data_reshaped(frame,marker,coordinate) = labeled_marker_data(marker,coordinate,frame);
        end
    end
end

savepath = fullfile([pwd,filesep,'qualisys_data_reshaped']);
save(savepath,'data_reshaped')
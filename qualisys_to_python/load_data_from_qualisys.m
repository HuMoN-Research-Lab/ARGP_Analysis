
sessionID = 'qualisys_sesh_2022-05-24_15_10_49_JSM_T2_slackline'; %sessionID name
qualisys_file_name = 'argp_pilot_2022_04_29_TDW.mat'; %Qualisys mat file name 

%change anything before 'FreeMocap_Data' to match your path 
filepath = fullfile('C:\Users\miken\OneDrive\Documents\GitHub\ARGP_Python_Pipeline\Data\' ,qualisys_file_name);

mat_data = load(filepath);


labeled_marker_data = mat_data.argp_pilot_2022_04_29_TDW.Trajectories.Labeled.Data; % Change the 'argp_pilot...' part of this path to match what's in your path

shape_marker_data = size(labeled_marker_data);

num_markers = shape_marker_data(1);
num_coordinates = 3;
num_frames = shape_marker_data(3);

test_data = labeled_marker_data(:,1:3,1:5);

mat_data_reshaped = nan(num_frames, num_markers, 3);


for frame = 1:num_frames
    for marker = 1:num_markers
        for coordinate = 1:num_coordinates
    mat_data_reshaped(frame,marker,coordinate) = labeled_marker_data(marker,coordinate,frame);
        end
    end
end

savepath = fullfile('C:\Users\miken\OneDrive\Documents\GitHub\ARGP_Python_Pipeline\Data\qualisys_markers_3d');
save(savepath,'mat_data_reshaped')
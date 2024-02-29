

import numpy as np

import matplotlib.pyplot as plt
import pickle
import cv2
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.ticker as mticker

from pathlib import Path 
from datetime import datetime




mediapipe_indices = [
    'nose',
    'left_eye_inner',
    'left_eye',
    'left_eye_outer',
    'right_eye_inner',
    'right_eye',
    'right_eye_outer',
    'left_ear',
    'right_ear',
    'mouth_left',
    'mouth_right',
    'left_shoulder',
    'right_shoulder',
    'left_elbow',
    'right_elbow',
    'left_wrist',
    'right_wrist',
    'left_pinky',
    'right_pinky',
    'left_index',
    'right_index',
    'left_thumb',
    'right_thumb',
    'left_hip',
    'right_hip',
    'left_knee',
    'right_knee',
    'left_ankle',
    'right_ankle',
    'left_heel',
    'right_heel',
    'left_foot_index',
    'right_foot_index'
    ]
    


#you can skip every 10th frame 
class skeleton_data_holder:
    def __init__(self, path_to_freemocap_data_folder, session_info):
    
        skeleton_type = session_info['skeleton_type']
        sessionID = session_info['sessionID']
        path_to_data_array_folder = path_to_freemocap_data_folder/sessionID/'DataArrays'

        self.run(path_to_data_array_folder,skeleton_type)
        f = 2

    def run(self,path_to_data_array_folder,skeleton_type):

        self.skeleton_XYZ_data = self.load_skeleton_XYZ_data(path_to_data_array_folder,skeleton_type)
        self.total_body_COM_data = self.load_total_body_COM_XYZ_data(path_to_data_array_folder)
        self.segment_COM_data = self.load_segment_COM_XYZ_data(path_to_data_array_folder)
        self.skeleton_connections_data = self.load_skeleton_connections_data(path_to_data_array_folder,skeleton_type)
         
    def load_skeleton_XYZ_data(self, path_to_data_array_folder, skeleton_type):

        skeleton_XYZ_file_name = 'mediaPipeSkel_3d_origin_aligned.npy'.format(skeleton_type)
        skeleton_XYZ_data = np.load(path_to_data_array_folder/skeleton_XYZ_file_name)

        return skeleton_XYZ_data
    
    def load_total_body_COM_XYZ_data(self,path_to_data_array_folder):

        total_body_COM_file_name = 'totalBodyCOM_frame_XYZ.npy'
        total_body_COM_data = np.load(path_to_data_array_folder/total_body_COM_file_name)

        return total_body_COM_data
    
    def load_segment_COM_XYZ_data(self,path_to_data_array_folder):

        segment_COM_file_name = 'segmentedCOM_frame_joint_XYZ.npy'
        segment_COM_XYZ_data = np.load(path_to_data_array_folder/segment_COM_file_name)

        return segment_COM_XYZ_data

    def load_skeleton_connections_data(self, path_to_data_array_folder,skeleton_type):

        skeleton_connections_file_name = 'mediapipe_skeleton_segments_dict.pkl'.format(skeleton_type)
    
        open_file = open(path_to_data_array_folder/skeleton_connections_file_name, "rb")
        skel_connections_XYZ = pickle.load(open_file)
        open_file.close()

        return skel_connections_XYZ


class video_loader:

    def __init__(self,path_to_freemocap_data_folder,session_info,num_frame_range):
        
        self.start_frame = num_frame_range[0]
        self.end_frame = num_frame_range[-1]
        sessionID = session_info['sessionID']
        
        self.run(path_to_freemocap_data_folder,sessionID)

    def run(self,path_to_freemocap_data_folder,sessionID):
        synced_vid_path = self.create_synced_vid_path(path_to_freemocap_data_folder,sessionID)
        cap = self.load_video_capture_object(synced_vid_path)
        self.video_frames_to_plot = self.get_video_frames_to_plot(cap)

        f = 2

    def get_video_frames_to_plot(self,cap):

        video_frames_to_plot = []
        frame = self.start_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
        while frame < self.end_frame:
            success, image = cap.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            video_frames_to_plot.append(image)
            frame += 1
        cap.release()

        return video_frames_to_plot    

    def create_synced_vid_path(self,path_to_freemocap_data_folder,sessionID):
        #synced_video_name = sessionID + '_annotated_video_1.mp4'
        #synced_vid_path = path_to_freemocap_data_folder/sessionID/'Annotated_Videos'/synced_video_name
        synced_video_name = sessionID + '_synced_Cam1.mp4'
        synced_vid_path = path_to_freemocap_data_folder/sessionID/'SyncedVideos'/synced_video_name
        return synced_vid_path

    def load_video_capture_object(self,synced_vid_path):
        cap = cv2.VideoCapture(str(synced_vid_path))
        return cap


class skeleton_data_for_plotting:
    def __init__(self, skeleton_data_class, num_frame_range, step_interval,skeleton_indices):
        
        #self.skeleton_data_class = skeleton_data_class
        self.num_frame_range = num_frame_range
        self.start_frame = num_frame_range[0]
        self.end_frame = num_frame_range[-1]
        self.step_interval = step_interval
        self.skeleton_indices = skeleton_indices

        self.run(skeleton_data_class,skeleton_indices)

    def run(self,skeleton_data_class,skeleton_indices):

        self.slice_skeleton_data_for_plotting(skeleton_data_class)

        self.right_foot_XYZ, self.right_foot_average_XYZ = self.get_skeleton_foot_data(skeleton_indices,'right')
        self.left_foot_XYZ, self.left_foot_average_XYZ = self.get_skeleton_foot_data(skeleton_indices,'left')
        self.back_foot_avg_position, self.front_foot_avg_position = self.get_anterior_posterior_bounds(self.left_foot_XYZ,self.right_foot_XYZ)
        self.num_frames_to_plot, self.num_frame_length = self.get_frames_to_plot(self.num_frame_range,self.step_interval)
        self.mx_com,self.my_com = self.get_mean_COM_values(self.total_body_COM_data)
        self.mx_skel, self.my_skel, self.mz_skel = self.get_mean_skeleton_values(self.skeleton_XYZ_data,self.num_frame_length)
        f = 2

    def slice_skeleton_data_for_plotting(self,skeleton_data_class):

        self.skeleton_XYZ_data = skeleton_data_class.skeleton_XYZ_data[self.start_frame:self.end_frame:self.step_interval,:,:]
        self.total_body_COM_data = skeleton_data_class.total_body_COM_data[self.start_frame:self.end_frame:self.step_interval,:]
        self.segment_COM_data = skeleton_data_class.segment_COM_data[self.start_frame:self.end_frame:self.step_interval,:,:]
        self.skel_connections_XYZ_data = skeleton_data_class.skeleton_connections_data[self.start_frame:self.end_frame:self.step_interval]




    def get_skeleton_foot_data(self,skeleton_indices, which_foot:str):

        toe_index = skeleton_indices.index('{}_foot_index'.format(which_foot))
        heel_index = skeleton_indices.index('{}_heel'.format(which_foot))

        toe_XYZ = self.skeleton_XYZ_data[:,toe_index,:]
        heel_XYZ = self.skeleton_XYZ_data[:,heel_index,:]

        foot_XYZ = [heel_XYZ, toe_XYZ]
        foot_average_XYZ = np.mean(foot_XYZ, axis = 0)

        return foot_XYZ, foot_average_XYZ

    def get_anterior_posterior_bounds(self,left_foot_data,right_foot_data):

        back_foot_avg_position = np.mean([left_foot_data[0],right_foot_data[0]],axis = 0)
        front_foot_avg_position = np.mean([left_foot_data[1],right_foot_data[1]],axis = 0)

        return back_foot_avg_position, front_foot_avg_position

    def get_frames_to_plot(self,num_frame_range, step_interval):

        num_frames_to_plot = int(np.floor(((num_frame_range[-1] - num_frame_range[0])/step_interval)))
        num_frames_to_plot = range(num_frames_to_plot)
        num_frame_length = (len(num_frames_to_plot)/step_interval)-1

        return num_frames_to_plot, num_frame_length

    def get_mean_COM_values(self,total_body_COM_data):

        mx_com = np.nanmean(total_body_COM_data[:,0])
        my_com = np.nanmean(total_body_COM_data[:,1])

        return mx_com,my_com

    def get_mean_skeleton_values(self,skeleton_data,num_frame_length):
        mx_skel = np.nanmean(skeleton_data[:,0:33,0])
        my_skel = np.nanmean(skeleton_data[:,0:33,1])
        mz_skel = np.nanmean(skeleton_data[int(num_frame_length/2),0:33,2])

        return mx_skel,my_skel,mz_skel
        f = 2 



class COM_plot_creator:

    def __init__(self,freemocap_session_path,freemocap_plotting_data,output_video_fps, video_frames_to_plot,stance):
        
        self.azimuth = -70
        self.stance = stance
        self.num_frame_range = freemocap_plotting_data.num_frame_range

        self.run(freemocap_session_path,freemocap_plotting_data,output_video_fps,video_frames_to_plot)


        f = 2
    def run(self,freemocap_session_path,freemocap_plotting_data,output_video_fps,video_frames_to_plot):

        self.time_array = self.create_time_array(freemocap_plotting_data.num_frames_to_plot,output_video_fps)
        self.freemocap_plotting_data = freemocap_plotting_data
        

        self.img_artist = None

        figure = self.create_figure()

        print('Starting Frame Animation') 
        ani = FuncAnimation(figure, self.animate, frames= freemocap_plotting_data.num_frames_to_plot, interval=.1, repeat=False, fargs = (video_frames_to_plot,), init_func= self.animation_init)
        writervideo = animation.FFMpegWriter(fps=output_video_fps)
        ani.save(freemocap_session_path/'medaipipe_testing_{}.mp4'.format(self.stance), writer=writervideo)
        print('Animation has been saved to {}'.format(freemocap_session_path))
        f=2

    def create_figure(self):

        figure = plt.figure(figsize=(10,10))
        figure.suptitle('Center of Mass (COM) Comparison', fontsize = 16, y = .94, color = 'royalblue')
        
        ax_3d = figure.add_subplot(3,2,(1,4), projection = '3d')
        ax_2d = figure.add_subplot(325)
        ax_video = figure.add_subplot(322)
        ax_1d_lateral = figure.add_subplot(326)
        ax_1d_ap = figure.add_subplot(326)

        l1, b1, w1, h1 = ax_3d.get_position().bounds
        ax_3d.set_position([l1-l1*.72,b1+b1*.1,w1,h1])
        l2, b2, w2, h2 = ax_2d.get_position().bounds
        ax_2d.set_position([l2+l2*.2,b2+b2*.95,w2,h2])
        l3, b3, w3, h3 = ax_video.get_position().bounds
        ax_video.set_position([l3,b3-b3*.15,w3,h3])
        l4, b4, w4, h4 = ax_1d_lateral.get_position().bounds
        ax_1d_lateral.set_position([l4+l4*.1,b4+b4*2,w4,h4*.5])
        l5, b5, w5, h5 = ax_1d_ap.get_position().bounds
        ax_1d_ap.set_position([l5+l5*.1,b5+b5*.5,w5,h5*.5])
   
        ax_video.axis('off')

        self.ax_3d = ax_3d
        self.ax_2d = ax_2d
        self.ax_video = ax_video
        self.ax_1d_lateral = ax_1d_lateral
        self.ax_1d_ap = ax_1d_ap

        self.mx_skel = self.freemocap_plotting_data.mx_skel
        self.my_skel = self.freemocap_plotting_data.my_skel
        self.mz_skel = self.freemocap_plotting_data.mz_skel

        self.mx_com = self.freemocap_plotting_data.mx_com
        self.my_com = self.freemocap_plotting_data.my_com

        self.skel_3d_range = 900
        self.com_2d_range= 500
        return figure
    
    def create_time_array(self,num_frames_to_plot,output_video_fps):
        time_array = []
        for frame_num in num_frames_to_plot:
            time_array.append(frame_num/output_video_fps)
        
        return time_array

    def clear_and_set_axes(self,frame,ax_3d,ax_2d,ax_1d_lat,ax_1d_ap,ax_video):
        ax_3d.cla()
        ax_2d.cla()
        ax_1d_lat.cla()
        ax_1d_ap.cla()
        
        ax_3d.set_title('Frame# {}'.format(str(self.num_frame_range[frame])),pad = -20, y = 1.)
        ax_3d.set_xlim([self.mx_skel-self.skel_3d_range, self.mx_skel+self.skel_3d_range]) #maybe set ax limits before the function? if we're using cla() they probably don't need to be redefined every time 
        ax_3d.set_ylim([self.my_skel-self.skel_3d_range, self.my_skel+self.skel_3d_range])
        ax_3d.set_zlim([self.mz_skel-self.skel_3d_range, self.mz_skel+self.skel_3d_range])
        
        self.azimuth = self.azimuth + .25
        ax_3d.view_init(elev = 0, azim = self.azimuth)

        ax_3d.xaxis.set_major_locator(mticker.MultipleLocator(400))
        ax_3d.xaxis.set_minor_locator(mticker.MultipleLocator(200))
        ax_3d.yaxis.set_major_locator(mticker.MultipleLocator(400))
        ax_3d.yaxis.set_minor_locator(mticker.MultipleLocator(200))
        ax_3d.zaxis.set_major_locator(mticker.MultipleLocator(400))
        ax_3d.zaxis.set_minor_locator(mticker.MultipleLocator(200))
        ax_3d.tick_params(axis='y', labelrotation = -9)
 

        ax_2d.set_title('Total Body COM Trajectory')
        ax_2d.set_xlim([self.mx_com-600, self.mx_com+600])
        ax_2d.set_ylim([self.my_com-600, self.my_com+600])
        ax_2d.set_aspect('equal', adjustable='box')

        ax_1d_lat.set_title('Max/Min Lateral COM Position vs. Time') 
        ax_1d_lat.set_ylim([self.mx_com-300, self.mx_com+300])
        ax_1d_lat.set_xlim(self.time_array[0],self.time_array[-1])
        #ax_1d_lat.set_xlim([self.time_array[frame]-5,self.time_array[frame]+5])
        ax_1d_lat.axes.xaxis.set_ticks([])

        ax_1d_ap.set_title('Anterior/Posterior COM Position vs. Time')
        ax_1d_ap.set_xlim(self.time_array[0],self.time_array[-1])
        #ax_1d_ap.set_xlim([self.time_array[frame]-5,self.time_array[frame]+5])
        ax_1d_ap.set_ylim([self.my_com-350, self.my_com+350])

        #ax_video.set_xlim([700,1300])
        #ax_video.set_ylim([1000,200])
        ax_video.axis('off')

        ax_1d_lat.set_ylabel('X Position (mm)')
        
        ax_1d_ap.set_xlabel('Time (s)')
        ax_1d_ap.set_ylabel('Y Position (mm)')
                
        ax_2d.set_xlabel('X Position (mm)')
        ax_2d.set_ylabel('Y Position (mm)')
        
        ax_3d.set_xlabel('X (mm)')
        ax_3d.set_ylabel('Y (mm)')
        ax_3d.set_zlabel('Z (mm)')

        #ax_3d.grid(False)
        #ax_3d.axis('off')

    
    def create_segment_connection(self,skeleton_connection_data,frame,segment):
        left_segment_name = 'left_' + segment
        right_segment_name = 'right_' + segment

        left_joint = skeleton_connection_data[frame][left_segment_name][0]
        right_joint = skeleton_connection_data[frame][right_segment_name][0]
        segment_connection_x, segment_connection_y, segment_connection_z = [[left_joint[0],right_joint[0]],[left_joint[1],right_joint[1]],[left_joint[2],right_joint[2]]]

        return segment_connection_x, segment_connection_y, segment_connection_z

    def plot_skeleton_bones(self,frame,ax_3d,ax_2d,skeleton_connection_data, color_str, alpha_val_3d = 1, alpha_val_2d = .4):
        this_frame_skeleton_data = skeleton_connection_data[frame]
        for segment in this_frame_skeleton_data.keys():
            prox_joint = this_frame_skeleton_data[segment][0] 
            dist_joint = this_frame_skeleton_data[segment][1]
            
            bone_x,bone_y,bone_z = [prox_joint[0],dist_joint[0]],[prox_joint[1],dist_joint[1]],[prox_joint[2],dist_joint[2]] 

            ax_3d.plot(bone_x,bone_y,bone_z,color = color_str, alpha = alpha_val_3d)

            ax_2d.plot(bone_x,bone_y, color = color_str, alpha = alpha_val_2d) #plot the bones transparently on the trajectory graph while we're at it 

    def plot_3d_segment_and_total_body_COM(self,frame,ax_3d,segment_COM_data,total_body_COM_data, alpha_val = 1):
        this_frame_segment_COM_data = segment_COM_data[frame,:,:]
        this_frame_total_body_COM_data = total_body_COM_data[frame,:]

        #ax_3d.scatter(this_frame_segment_COM_data[:,0],this_frame_segment_COM_data[:,1],this_frame_segment_COM_data[:,2], color = 'orange', label = 'Segment COM',alpha = alpha_val)
        ax_3d.scatter(this_frame_total_body_COM_data[0],this_frame_total_body_COM_data[1], this_frame_total_body_COM_data[2], color = 'magenta', label = 'Total Body COM', marker = '*', s = 70, edgecolor = 'purple', alpha = alpha_val)


    def plot_3d_line(self,data_x,data_y,data_z,ax, color_str = 'black', alpha_val = 1):
        ax.plot(data_x,data_y,data_z,color = color_str, alpha = alpha_val)
        
    def plot_2d_line(self,data_x,data_y,ax, alpha_val = .4, color_str = 'grey'):
        ax.plot(data_x,data_y,color = color_str, alpha = alpha_val)

    def animation_init(self):
        #the FuncAnimation needs an initial function that it will run, otherwise it will run animate() twice for frame 0 
        pass  

    def get_this_frame_foot_data(self,frame,foot_data):
        this_frame_foot_data_x = [foot_data[0][frame][0],foot_data[1][frame][0]]
        this_frame_foot_data_y = [foot_data[0][frame][1],foot_data[1][frame][1]]

        return this_frame_foot_data_x, this_frame_foot_data_y

    def plot_BOS_bounds(self,frame,ax_2d,skeleton_data_class, alpha_val_dark, alpha_val_lite):
        
            this_frame_left_foot_x, this_frame_left_foot_y = self.get_this_frame_foot_data(frame,self.freemocap_plotting_data.left_foot_XYZ)
            this_frame_right_foot_x, this_frame_right_foot_y = self.get_this_frame_foot_data(frame,self.freemocap_plotting_data.right_foot_XYZ)

            ax_2d.plot(this_frame_left_foot_x,this_frame_left_foot_y,color = 'blue', label= 'Max Lateral Bound (Left Foot)')
            ax_2d.plot(this_frame_right_foot_x,this_frame_right_foot_y,color = 'red',label= 'Max Lateral Bound (Right Foot)')

            ax_2d.plot([this_frame_left_foot_x[0],this_frame_right_foot_x[0]],[this_frame_left_foot_y[0],this_frame_right_foot_y[0]], color = 'coral', label = 'Posterior Bound', alpha = alpha_val_lite, linestyle = '--')
            ax_2d.plot([this_frame_left_foot_x[1],this_frame_right_foot_x[1]],[this_frame_left_foot_y[1],this_frame_right_foot_y[1]], color = 'forestgreen', label = 'Anterior Bound', alpha = alpha_val_lite, linestyle = '--')

    def plot_BOS_right_leg_bound(self,frame,ax_2d,skeleton_data_class, alpha_val_dark, alpha_val_lite):
            this_frame_right_foot_x, this_frame_right_foot_y = self.get_this_frame_foot_data(frame,self.freemocap_plotting_data.right_foot_XYZ)
            ax_2d.plot(this_frame_right_foot_x,this_frame_right_foot_y,color = 'red',label= 'Max Lateral Bound (Right Foot)')

            ax_2d.plot(this_frame_right_foot_x[0],this_frame_right_foot_y[0], color = 'coral', marker = 'o', ms = 4, alpha = alpha_val_lite, label = 'Posterior Bound') #left leg one leg stance plotting
            ax_2d.plot(this_frame_right_foot_x[1],this_frame_right_foot_y[1], color = 'forestgreen', marker = 'o', ms = 4, alpha = alpha_val_lite, label = 'Anterior Bound') #left leg one leg stance plotting


    def plot_future_COM_and_lateral_BOS_positions(self,ax_1d_lat,skeleton_data_class, alpha_val=.5):
            
            if self.stance == 'natural':
                ax_1d_lat.plot(self.time_array,skeleton_data_class.total_body_COM_data[:,0],color = 'lightgrey', alpha = alpha_val)
                ax_1d_lat.plot(self.time_array,skeleton_data_class.left_foot_average_XYZ[:,0], color = 'paleturquoise', alpha = alpha_val)
                ax_1d_lat.plot(self.time_array,skeleton_data_class.right_foot_average_XYZ[:,0], color = 'lightpink', alpha = alpha_val)

            elif self.stance == 'right_leg':
                ax_1d_lat.plot(self.time_array,skeleton_data_class.total_body_COM_data[:,0],color = 'lightgrey', alpha = alpha_val)
                ax_1d_lat.plot(self.time_array,skeleton_data_class.right_foot_average_XYZ[:,0], color = 'lightpink', alpha = alpha_val)

    def plot_current_COM_and_lateral_BOS_positions(self,frame,ax_1d_lat,skeleton_data_class, alpha_val=1):
            if self.stance == 'natural':
                ax_1d_lat.plot(self.time_array[0:frame+1],skeleton_data_class.left_foot_average_XYZ[0:frame+1,0], color = 'blue', alpha = alpha_val)
                ax_1d_lat.plot(self.time_array[0:frame+1],skeleton_data_class.right_foot_average_XYZ[0:frame+1,0], color = 'red', alpha = alpha_val)
                ax_1d_lat.plot(self.time_array[0:frame+1],skeleton_data_class.total_body_COM_data[0:frame+1,0], color = 'grey', alpha = alpha_val)

            elif self.stance == 'right_leg':
                ax_1d_lat.plot(self.time_array[0:frame+1],skeleton_data_class.right_foot_average_XYZ[0:frame+1,0], color = 'red', alpha = alpha_val)
                ax_1d_lat.plot(self.time_array[0:frame+1],skeleton_data_class.total_body_COM_data[0:frame+1,0], color = 'grey', alpha = alpha_val)
    
    def plot_current_COM_and_antpos_BOS_positions(self,frame,ax_1d_ap,skeleton_data_class, alpha_val=1):
            if self.stance == 'natural':
                ax_1d_ap.plot(self.time_array[0:frame+1],skeleton_data_class.front_foot_avg_position[0:frame+1,1], color = 'forestgreen', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array[0:frame+1],skeleton_data_class.back_foot_avg_position[0:frame+1,1], color = 'coral', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array[0:frame+1],skeleton_data_class.total_body_COM_data[0:frame+1,1], color = 'grey', alpha = alpha_val)

            elif self.stance == 'right_leg':
                this_frame_right_foot_x, this_frame_right_foot_y = self.get_this_frame_foot_data(frame,self.freemocap_plotting_data.right_foot_XYZ)
                
                ax_1d_ap.plot(self.time_array[0:frame+1],self.freemocap_plotting_data.right_foot_XYZ[1][0:frame+1,1], color = 'forestgreen', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array[0:frame+1],self.freemocap_plotting_data.right_foot_XYZ[0][0:frame+1,1], color = 'coral', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array[0:frame+1],skeleton_data_class.total_body_COM_data[0:frame+1,1], color = 'grey', alpha = alpha_val)
            
    def plot_future_COM_and_antpos_BOS_positions(self,ax_1d_ap,skeleton_data_class, alpha_val=.5):
    
            if self.stance == 'natural':
                ax_1d_ap.plot(self.time_array,skeleton_data_class.front_foot_avg_position[:,1], color = 'forestgreen', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array,skeleton_data_class.back_foot_avg_position[:,1], color = 'coral', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array,skeleton_data_class.total_body_COM_data[:,1], color = 'grey', alpha = alpha_val)
            
            elif self.stance == 'right_leg':
                
                ax_1d_ap.plot(self.time_array,skeleton_data_class.right_foot_XYZ[1][:,1], color = 'forestgreen', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array,skeleton_data_class.right_foot_XYZ[0][:,1], color = 'coral', alpha = alpha_val)
                ax_1d_ap.plot(self.time_array,skeleton_data_class.total_body_COM_data[:,1], color = 'grey', alpha = alpha_val)

    def animate(self,frame,video_frames_to_plot):

        ax_3d = self.ax_3d
        ax_2d = self.ax_2d 
        ax_video = self.ax_video
        ax_1d_lat = self.ax_1d_lateral
        ax_1d_ap = self.ax_1d_ap
        
        
        freemocap_bone_color = 'magenta'
        if frame % 100 == 0:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Currently on frame: {} at {}".format(frame,current_time))

        self.clear_and_set_axes(frame,ax_3d,ax_2d,ax_1d_lat,ax_1d_ap,ax_video)

        freemocap_hip_connection_x,freemocap_hip_connection_y,freemocap_hip_connection_z = self.create_segment_connection(self.freemocap_plotting_data.skel_connections_XYZ_data,frame,'thigh')
        freemocap_shoulder_connection_x,freemocap_shoulder_connection_y,freemocap_shoulder_connection_z = self.create_segment_connection(self.freemocap_plotting_data.skel_connections_XYZ_data,frame,'upper_arm')
        
        self.plot_skeleton_bones(frame,ax_3d,ax_2d,self.freemocap_plotting_data.skel_connections_XYZ_data, color_str = freemocap_bone_color)

        self.plot_3d_line(freemocap_hip_connection_x,freemocap_hip_connection_y,freemocap_hip_connection_z,ax_3d,color_str  = freemocap_bone_color)
        self.plot_3d_line(freemocap_shoulder_connection_x,freemocap_shoulder_connection_y,freemocap_shoulder_connection_z,ax_3d, color_str  = freemocap_bone_color)

        ax_3d.scatter(self.freemocap_plotting_data.skeleton_XYZ_data[frame,:,0],self.freemocap_plotting_data.skeleton_XYZ_data[frame,:,1],self.freemocap_plotting_data.skeleton_XYZ_data[frame,:,2],color = 'darkmagenta', label = 'MediaPipe')

        self.plot_3d_segment_and_total_body_COM(frame,ax_3d,self.freemocap_plotting_data.segment_COM_data,self.freemocap_plotting_data.total_body_COM_data)

        tail_length = 120
        plot_fade_frame = frame - tail_length

        self.plot_2d_line(freemocap_hip_connection_x,freemocap_hip_connection_y,ax_2d, color_str = freemocap_bone_color)
        self.plot_2d_line(freemocap_shoulder_connection_x,freemocap_shoulder_connection_y,ax_2d, color_str= freemocap_bone_color)


        if plot_fade_frame < 0:
            ax_2d.plot(self.freemocap_plotting_data.total_body_COM_data[0:frame,0],self.freemocap_plotting_data.total_body_COM_data[0:frame,1],color = 'grey')
        else:
            ax_2d.plot(self.freemocap_plotting_data.total_body_COM_data[plot_fade_frame:frame,0],self.freemocap_plotting_data.total_body_COM_data[plot_fade_frame:frame,1],color = 'grey')

        ax_2d.plot(self.freemocap_plotting_data.total_body_COM_data[frame,0],self.freemocap_plotting_data.total_body_COM_data[frame,1],marker = '*', color = 'magenta', markeredgecolor = 'purple', ms = 8)


        if self.stance == 'natural':
            self.plot_BOS_bounds(frame,ax_2d,self.freemocap_plotting_data,1,.3)
            #plot the future x positions of the COM and lateral BOS bounds 
            self.plot_future_COM_and_lateral_BOS_positions(ax_1d_lat,self.freemocap_plotting_data)

            ax_1d_lat.axvline(self.time_array[frame], color = 'black')
            #plot current x positions 
            
            self.plot_current_COM_and_lateral_BOS_positions(frame,ax_1d_lat,self.freemocap_plotting_data,.5)
            self.plot_future_COM_and_antpos_BOS_positions(ax_1d_ap,self.freemocap_plotting_data)

            ax_1d_ap.axvline(self.time_array[frame], color = 'black')

            self.plot_current_COM_and_antpos_BOS_positions(frame,ax_1d_ap,self.freemocap_plotting_data,.5)
  
        
        if self.stance == 'right_leg':
            self.plot_BOS_right_leg_bound(frame,ax_2d,self.freemocap_plotting_data,1,.5)
            self.plot_future_COM_and_lateral_BOS_positions(ax_1d_lat,self.freemocap_plotting_data)

            ax_1d_lat.axvline(self.time_array[frame], color = 'black')

            self.plot_current_COM_and_lateral_BOS_positions(frame,ax_1d_lat,self.freemocap_plotting_data,.5)

            self.plot_future_COM_and_antpos_BOS_positions(ax_1d_ap,self.freemocap_plotting_data)

            ax_1d_ap.axvline(self.time_array[frame], color = 'black')

            self.plot_current_COM_and_antpos_BOS_positions(frame,ax_1d_ap,self.freemocap_plotting_data,.5)

        ax_1d_lat.plot(self.time_array[frame],self.freemocap_plotting_data.total_body_COM_data[frame,0], '*', color = 'magenta', ms = 8, markeredgecolor = 'purple')
        ax_1d_ap.plot(self.time_array[frame],self.freemocap_plotting_data.total_body_COM_data[frame,1], '*', color = 'magenta', ms = 8, markeredgecolor = 'purple')


        video_frame = video_frames_to_plot.video_frames_to_plot[frame]
        if self.img_artist is None:
            self.img_artist = ax_video.imshow(video_frame)
        else:
            self.img_artist.set_data(video_frame)

        a = ax_3d.get_legend_handles_labels()
        b = {l:h for h,l in zip(*a)}
        c = [*zip(*b.items())]              # c = [(l1 l2) (h1 h2)]
        d = c[::-1]
        ax_3d.legend(*d,bbox_to_anchor=(.24, -0.53))

        a1 = ax_2d.get_legend_handles_labels()
        b1 = {l:h for h,l in zip(*a1)}
        c1 = [*zip(*b1.items())]              # c = [(l1 l2) (h1 h2)]
        d1 = c1[::-1]
        ax_2d.legend(*d1,fontsize = 10, bbox_to_anchor=(1.15, -.55),ncol = 2)  


        f = 2   
if __name__ == '__main__':

    path_to_freemocap_data_folder = Path(r"D:\Dropbox\FreeMoCapProject\FreeMocap_Data")

    
    session_one_info = {'sessionID':'sesh_2022-09-19_16_16_50_in_class_jsm','skeleton_type':'mediapipe'}
    freemocap_session_path = path_to_freemocap_data_folder / session_one_info['sessionID']

    # stance = 'natural'
    stance = 'left_leg'
    step_interval = 1 #leave at 1 unless using qualisys (step interval refers to skipping frames in the plotting to have the output video fps match for qualisys and mediapipe)
    output_video_fps = 30
    
    if stance == 'natural':
        mediapipe_num_frame_range = range(0,1100)
    elif stance == 'left_leg':
        mediapipe_num_frame_range = range(0,1100) #for webcam natural
    elif stance == 'right_leg':
        mediapipe_num_frame_range = range(0,1100) #for webcam natural


    #load all the marker and COM data into a class
    mediapipe_data_holder = skeleton_data_holder(path_to_freemocap_data_folder, session_one_info)

    #calculate all the data that we need to plot (i.e. anterior/posterior/medial/later bounds, mean data etc.)
    mediapipe_data_to_plot = skeleton_data_for_plotting(mediapipe_data_holder,mediapipe_num_frame_range,step_interval,mediapipe_indices)
    
    #Don't really remember why I did this, I think just to load the body/pose data to be plotted (aaron - 09_20_22)
    mediapipe_data_to_plot.skeleton_XYZ_data = mediapipe_data_to_plot.skeleton_XYZ_data[:,0:33,:]


    print('Loading video data')
    video_frames_to_plot = video_loader(path_to_freemocap_data_folder,session_one_info,mediapipe_num_frame_range)

    COM_plot = COM_plot_creator(freemocap_session_path,mediapipe_data_to_plot,output_video_fps,video_frames_to_plot, stance)
    
    f=2


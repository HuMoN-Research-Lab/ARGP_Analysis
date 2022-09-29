
def dumb_qualisys_joint_center_dictionary_builder() -> dict:

    # this is a special purpose dictionary for getting ARGP skeleton data from qualisys
    # into a generic meadiapipe++ format

    # below is a handwritten dictionary, where the key represents the joint center name
    # that is going into the skeleton, the first value represents the physical qualisys
    # markers that are being combined to be put into the joint center, and the second value
    # (or array of values) is the relative weight of each of the markers for the joint

    qualisys_joint_center_dict = {
        "head_xyz": [["HeadL+HeadR"], [0.5, 0.5]],
        "left_head_marker_xyz": [["HeadL"], [1]],
        "right_head_marker_xyz": [["HeadR"], [1]],
        "left_wrist_xyz": [["LWristOut+LWristIn"], [0.5, 0.5]],
        "right_wrist_xyz": [["RWristOut+RWristIn"], [0.5, 0.5]],
        "left_hand_xyz": [["LHandOut"], [1]],
        "right_hand_xyz": [["RHandOut"], [1]],
        "left_shoulder_xyz": [["LShoulderFront+LShoulderBack"], [0.5, 0.5]],
        "cspine_xyz": [["left_shoulder_xyz+right_shoulder_xyz"], [0.5, 0.5]],
        "left_elbow_xyz": [["LElbowIn+LElbowOut"], [0.5, 0.5]],
        "right_elbow_xyz": [["RElbowIn+RElbowOut"], [0.5, 0.5]],
        "left_knee_xyz": [["LKneeIn+LKneeOut"], [0.5, 0.5]],
        "right_knee_xyz": [["RKneeIn+RKneeOut"], [0.5, 0.5]],
        "left_ankle_xyz": [["LAnkleIn+LAnkleOut"], [0.5, 0.5]],
        "right_ankle_xyz": [["RAnkleIn+RAnkleOut"], [0.5, 0.5]],
        "left_foot_xyz": [["?"], ["?"]],
        "right_foot_xyz": [["?"], ["?"]],
        "left_heel_xyz": [["LHeel"], [1]],
        "right_heel_xyz": [["RHeel"], [1]],
        "left_hip_xyz": [["LHipFront+LHipBack"], [0.5, 0.5]],
        "right_hip_xyz": [["RHipFront+RHipBack"], [0.5, 0.5]],
        "right_shoulder_xyz": [["RShoulderFront+RShoulderBack"], [0.5, 0.5]]
    }

    return qualisys_joint_center_dict

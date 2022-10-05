
qualisys_joint_center_dict = {

        "head_xyz": {
                "HeadL": 0.5,
                "HeadR": 0.5
        },

        "left_head_xyz": {
                "HeadL": 1
        },

        "right_head_xyz": {
                "HeadR": 1
        },

        "left_wrist_xyz": {
                "LWristOut": 0.5,
                "LWristIn": 0.5
        },

        "right_wrist_xyz": {
                "RWristOut": 0.5,
                "RWristIn": 0.5
        },

        "left_hand_xyz": {
                "LHandOut": 1
        },

        "right_hand_xyz": {
                "RHandOut": 1
        },

        "left_shoulder_xyz": {
                "LShoulderFront": 0.5,
                "LShoulderBack": 0.5
        },

        "right_shoulder_xyz": {
                "RShoulderFront": 0.5,
                "RShoulderBack": 0.5
        },

        "cspine_xyz": {
            "RShoulderBack": 0.25,
            "LShoulderBack": 0.25,
            "RShoulderFront": 0.25,
            "LShoulderFront": 0.25
        },

        "left_elbow_xyz": {
                "LElbowIn": 0.5,
                "LElbowOut": 0.5
        },


        "right_elbow_xyz": {
                "RElbowIn": 0.5,
                "RElbowOut": 0.5
        },

        "left_knee_xyz": {
                "LKneeIn": 0.5,
                "LKneeOut": 0.5
        },

        "right_knee_xyz": {
                "RKneeIn": 0.5,
                "RKneeOut": 0.5
        },

        "left_ankle_xyz": {
                "LAnkleIn": 0.5,
                "LAnkleOut": 0.5
        },

        "right_ankle_xyz": {
                "RAnkleIn": 0.5,
                "RAnkleOut": 0.5
        },

        "left_foot_xyz": {
                "LToeTip": 0.334,
                "LForefootIn": 0.333,
                "LForefootOut": 0.333
        },

        "right_foot_xyz": {
                "RToeTip": 0.334,
                "RForefootIn": 0.333,
                "RForefootOut": 0.333
        },

        "left_heel_xyz": {
                "LHeel": 1
        },

        "right_heel_xyz": {
                "RHeel": 1
        },

        "left_hip_xyz": {
                "WaistLFront": 0.5,
                "WaistLBack": 0.5
        },

        "right_hip_xyz": {
                "WaistRFront": 0.5,
                "WaistRBack": 0.5
        }
        }

# def dumb_qualisys_joint_center_dictionary_builder() -> dict:
#
#     # this is a special purpose dictionary for getting ARGP skeleton data from qualisys
#     # into a generic meadiapipe++ format
#
#     # below is a handwritten dictionary, where the key represents the joint center name
#     # that is going into the skeleton, the first value represents the physical qualisys
#     # markers that are being combined to be put into the joint center, and the second value
#     # (or array of values) is the relative weight of each of the markers for the joint
#
#     qualisys_joint_center_dict = {
#         "head_xyz": [["HeadL+HeadR"], [0.5, 0.5]],
#         "left_head_marker_xyz": [["HeadL"], [1]],
#         "right_head_marker_xyz": [["HeadR"], [1]],
#         "left_wrist_xyz": [["LWristOut+LWristIn"], [0.5, 0.5]],
#         "right_wrist_xyz": [["RWristOut+RWristIn"], [0.5, 0.5]],
#         "left_hand_xyz": [["LHandOut"], [1]],
#         "right_hand_xyz": [["RHandOut"], [1]],
#         "left_shoulder_xyz": [["LShoulderFront+LShoulderBack"], [0.5, 0.5]],
#         "right_shoulder_xyz": [["RShoulderFront+RShoulderBack"], [0.5, 0.5]],
#         "old_cspine_xyz": [["RShoulderBack+LShoulderBack+RShoulderFront+LShoulderFront"], [0.25, 0.25, 0.25, 0.25]],  # This used to be[["left_shoulder_xyz+right_shoulder_xyz"], [0.5, 0.5]],
#
#         "cspine_xyz": {  # use this format for everything!
#             "RShoulderBack": 0.25,
#             "LShoulderBack": 0.25,
#             "RShoulderFront": 0.25,
#             "LShoulderFront": 0.25
#         },
#
#         "left_elbow_xyz": [["LElbowIn+LElbowOut"], [0.5, 0.5]],
#         "right_elbow_xyz": [["RElbowIn+RElbowOut"], [0.5, 0.5]],
#         "left_knee_xyz": [["LKneeIn+LKneeOut"], [0.5, 0.5]],
#         "right_knee_xyz": [["RKneeIn+RKneeOut"], [0.5, 0.5]],
#         "left_ankle_xyz": [["LAnkleIn+LAnkleOut"], [0.5, 0.5]],
#         "right_ankle_xyz": [["RAnkleIn+RAnkleOut"], [0.5, 0.5]],
#         "left_foot_xyz": [["LToeTip+LForefootIn+LForefootOut"], [0.334, 0.333, 0.333]],
#         "right_foot_xyz": [["RToeTip+RForefootIn+RForefootOut"], [0.334, 0.333, 0.333]],
#         "left_heel_xyz": [["LHeel"], [1]],
#         "right_heel_xyz": [["RHeel"], [1]],
#         "left_hip_xyz": [["WaistLFront+WaistLBack"], [0.5, 0.5]],
#         "right_hip_xyz": [["WaistRFront+WaistRBack"], [0.5, 0.5]]
#         }
#
#     return qualisys_joint_center_dict

 export CUDA_VISIBLE_DEVICES=1 
 unset CUDA_VISIBLE_DEVICES 
 
     --headless 

tensorboard --logdir=/home/jyz/project/Hahalim/HOVER/logs/teacher/wave_left07_poses --port 6008

# 设置环境变量，仅使用cuda:0
import os
import torch
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# stable_punch
# teacher
~/project/IsaacLab/isaaclab.sh -p  scripts/rsl_rl/train_teacher_policy.py \
    --num_envs 1024 \
    --reference_motion_path neural_wbc/data/data/motions/stable_punch.pkl

~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/play.py     --num_envs 10     --reference_motion_path neural_wbc/data/data/motions/stable_punch.pkl     --teacher_policy.resume_path neural_wbc/data/data/policy/h1:teacher     --teacher_policy.checkpoint model_16000.pt

# student
~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/train_student_policy.py \
    --num_envs 10 \
    --reference_motion_path neural_wbc/data/data/motions/stable_punch.pkl \
    --teacher_policy.resume_path neural_wbc/data/data/policy/h1:teacher \
    --teacher_policy.checkpoint model_16000.pt

 ~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/play.py     --num_envs 10     --reference_motion_path neural_wbc/data/data/motions/stable_punch.pkl     --student_player     --student_path neural_wbc/data/data/policy/h1:student     --student_checkpoint model_63000.pt
# ----------------------------------------------------------------------------------------------------------------------------------------------------
 # wave_left07_poses  wave_right07_poses  wave_both07_poses  guitar_right01_poses  hook_right_poses  greeting-08-shakehands-hamada_poses
 # teacher
 ~/project/IsaacLab/isaaclab.sh -p  scripts/rsl_rl/train_teacher_policy.py \
    --num_envs 1024 \
    --reference_motion_path neural_wbc/data/data/motions/guitar_right01_poses.pkl


# resume
~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/train_teacher_policy.py\
    --num_envs 4096\
    --reference_motion_path neural_wbc/data/data/motions/wave_right07_poses.pkl\
    --teacher_policy.resume_path logs/teacher/right2\
    --teacher_policy.checkpoint model_18500.pt

# teacher play
~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/play.py     --num_envs 10     --reference_motion_path neural_wbc/data/data/motions/wave_right07_poses.pkl     --teacher_policy.resume_path logs/teacher/wave_right07_poses3  --teacher_policy.checkpoint model_40500.pt

~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/play.py     --num_envs 10     --reference_motion_path neural_wbc/data/data/motions/greeting-08-shakehands-hamada_poses.pkl     --teacher_policy.resume_path logs/teacher/greeting-08-shakehands-hamada_poses    --teacher_policy.checkpoint model_89500.pt

# student
~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/train_student_policy.py \
    --num_envs 2048 \
    --reference_motion_path neural_wbc/data/data/motions/greeting-08-shakehands-hamada_poses.pkl \
    --teacher_policy.resume_path logs/teacher/greeting-08-shakehands-hamada_poses\
    --teacher_policy.checkpoint model_89500.pt


# resume
~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/train_student_policy.py \
    --num_envs 4096 \
    --reference_motion_path neural_wbc/data/data/motions/greeting-08-shakehands-hamada_poses.pkl \
    --teacher_policy.resume_path logs/teacher/greeting-08-shakehands-hamada_poses \
    --teacher_policy.checkpoint model_89500.pt\
    --student_policy.resume_path logs/teacher/greeting-08-shakehands-hamada_poses \
    --student_policy.checkpoint model_49500.pt


# student play
~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/play.py     --num_envs 1     --reference_motion_path neural_wbc/data/data/motions/wave_both07_poses.pkl     --student_player     --student_path logs/student/wave_both07_poses    --student_checkpoint model_82000.pt
# ----------------------------------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# eval
 ~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/eval.py \
    --num_envs 10 \
    --teacher_policy.resume_path logs/teacher/stable_punch \
    --teacher_policy.checkpoint model_15500.pt

 ~/project/IsaacLab/isaaclab.sh -p scripts/rsl_rl/eval.py \
    --num_envs 10 \
    --teacher_policy.resume_path logs/teacher/guitar_right01_poses \
    --teacher_policy.checkpoint model_53000.pt\
    --reference_motion_path neural_wbc/data/data/motions/guitar_right01_poses.pkl

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# sim-sim  --headless 
 ~/project/IsaacLab/isaaclab.sh -p neural_wbc/inference_env/scripts/mujoco_viewer_player.py

 ~/project/IsaacLab/isaaclab.sh -p neural_wbc/inference_env/scripts/eval.py \
    --num_envs 1 \
    --student_path logs/teacher/stable_punch \
    --student_checkpoint model_15500.pt

 ~/project/IsaacLab/isaaclab.sh -p neural_wbc/inference_env/scripts/eval.py\
    --num_envs 10\
    --student_path logs/student/hook_right_poses\
    --student_checkpoint model_113500.pt\
    --reference_motion_path neural_wbc/data/data/motions/hook_right_poses.pkl


# test
 ~/project/IsaacLab/isaaclab.sh -p neural_wbc/inference_env/scripts/eval.py\
    --num_envs 10\
    --student_path logs/student/guitar_right01_poses\
    --student_checkpoint model_89000.pt\
    --reference_motion_path neural_wbc/data/data/motions/guitar_right01_poses.pkl\
    --headless



 








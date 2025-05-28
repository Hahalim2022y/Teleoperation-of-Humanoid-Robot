# Research on Teleoperation of Humanoid Robot’s upper body Based on Reinforcement Learning

[![IsaacSim](https://img.shields.io/badge/IsaacSim-4.5.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Isaac Lab](https://img.shields.io/badge/IsaacLab-2.0.0-silver)](https://isaac-sim.github.io/IsaacLab)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://docs.python.org/3/whatsnew/3.10.html)
[![Linux platform](https://img.shields.io/badge/ubuntu-22.04-red)](https://releases.ubuntu.com/22.04/)


# Installation

1. Install Isaac Lab, see the [installation guide](https://isaac-sim.github.io/IsaacLab/v2.0.0/source/setup/installation/index.html).
    **Note**: Currently we has been tested with Isaac Lab versions 2.0.0. After you clone the Isaac Lab
    repository, check out the specific tag before installation. Also note that the `rsl_rl`
    package is renamed to `rsl_rl_lib` with the current `v2.0.0` tag of Isaac Lab, causing installation issues.
    This will be fixed once a new tag is created on the Isaac Lab repo.
    This error would not affect this repo, as we have our own customized `rsl_rl` package.
    ```bash
    git fetch origin
    git checkout v2.0.0
    ```
2. Define the following environment variable to specify the path to your IsaacLab installation:
    ```bash
    # Set the ISAACLAB_PATH environment variable to point to your IsaacLab installation directory
    export ISAACLAB_PATH=<your_isaac_lab_path>
    ```
3. Clone the repo and its submodules:
    ```bash
    git clone --recurse-submodules <REPO_URL>
    ```
4. Install this repo and its dependencies by running the following command from the root of this
   repo:
    ```bash
    ./install_deps.sh
    ```

# Training
## Teacher Policy
reference_motion_path can be set to stable_punch.pkl, wave_left07_poses.pkl, wave_right07_poses.pkl, wave_both07_poses.pkl, guitar_right01_poses.pkl, hook_right_poses.pkl, greeting-08-shakehands-hamada_poses.pkl

```bash
${ISAACLAB_PATH:?}/isaaclab.sh -p scripts/rsl_rl/train_teacher_policy.py \
    --num_envs 1024 \
    --reference_motion_path neural_wbc/data/data/motions/wave_left07_poses.pkl
```

The teacher policy is trained for 10000000 iterations, or until the user interrupts the training. The resulting checkpoint is stored in `neural_wbc/data/data/policy/h1:teacher/` and the filename is `model_<iteration_number>.pt`.


## Student Policy

```bash
${ISAACLAB_PATH:?}/isaaclab.sh -p scripts/rsl_rl/train_student_policy.py \
    --num_envs 1024 \
    --reference_motion_path neural_wbc/data/data/motions/wave_left07_poses.pkl \
    --teacher_policy.resume_path neural_wbc/data/data/policy/h1:teacher \
    --teacher_policy.checkpoint model_71500.pt
```
This assumes that you have already trained the teacher policy as there is no provided teacher policy in the repo. Change the filename to match the checkpoint you trained.


# Testing

## Play Teacher Policy

```bash
${ISAACLAB_PATH:?}/isaaclab.sh -p scripts/rsl_rl/play.py \
    --num_envs 10 \
    --reference_motion_path neural_wbc/data/data/motions/wave_left07_poses.pkl \
    --teacher_policy.resume_path neural_wbc/data/data/policy/h1:teacher \
    --teacher_policy.checkpoint model_71500.pt
```

## Play Student Policy

```bash
${ISAACLAB_PATH:?}/isaaclab.sh -p scripts/rsl_rl/play.py \
    --num_envs 10 \
    --reference_motion_path neural_wbc/data/data/motions/wave_left07_poses.pkl \
    --student_player \
    --student_path neural_wbc/data/data/policy/h1:student \
    --student_checkpoint model_100000.pt
```

# Evaluation

The evaluation iterates through all the reference motions included in the dataset specified by the
`--reference_motion_path` option and exits when all motions are evaluated. Randomization is turned
off during evaluation. At the end of execution, the script summarizes the results with the following
reference motion tracking metrics:


* **Success Rate [%]**: The percentage of motion tracking episodes that are successfully completed. An
    episode is considered successful if it follows the reference motion from start to finish without
    losing balance and avoiding collisions on specific body parts.
* **mpjpe_g [mm]**: The global mean per-joint position error, which measures the policy's ability to
    imitate the reference motion globally.
* **mpjpe_l [mm]**: The root-relative mean per-joint position error, which measures the policy's ability
    to imitate the reference motion locally.
* **mpjpe_pa [mm]**: The procrustes aligned mean per-joint position error, which aligns the links with
    the ground truth before calculating the errors.
* **accel_dist [mm/frame^2]**: The average joint acceleration error.
* **vel_dist [mm/frame]**: The average joint velocity error.
* **upper_body_joints_dist [radians]**: The average distance between the predicted and ground truth upper body joint positions.
* **lower_body_joints_dist [radians]**: The average distance between the predicted and ground truth lower body joint positions.
* **root_r_error [radians]**: The average torso roll error.
* **root_p_error [radians]**: The average torso pitch error.
* **root_y_error [radians]**: The average torso yaw error.
* **root_vel_error [m/frame]**: The average torso velocity error.
* **root_height_error [m]**: The average torso height error.


```bash
${ISAACLAB_PATH}/isaaclab.sh -p scripts/rsl_rl/eval.py \
    --num_envs 10 \
    --teacher_policy.resume_path neural_wbc/data/data/policy/h1:teacher \
    --teacher_policy.checkpoint model_<iteration_number>.pt
```


## Sim-to-Sim Validation

We also provide a [Mujoco environment](./neural_wbc/mujoco_wrapper/) for conducting sim-to-sim validation of the trained policy.
To run the evaluation of Sim2Sim

```bash
${ISAACLAB_PATH:?}/isaaclab.sh -p neural_wbc/inference_env/scripts/eval.py \
    --num_envs 1 \
    --headless \
    --student_path neural_wbc/data/data/policy/h1:student/ \
    --student_checkpoint model_<iteration_number>.pt
```

Please be aware that the `mujoco_wrapper` only supports one environment at a time. For a reference, it will take up to `5h` to evaluate `8k` reference motions. The inference_env is designed for maximum versatility.



## Running Scripts from an Isaac Lab Docker Container

You can run scripts in a Docker container without using the Isaac Sim GUI. Follow these steps:

1. **Install the NVIDIA Container Toolkit**:
   - Follow the installation guide [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

2. **Access the NGC Container Registry**:
   - Ensure you have access by following the instructions [here](https://docs.nvidia.com/ngc/gpu-cloud/ngc-private-registry-user-guide/index.html#accessing-ngc-registry).

3. **Start the Docker Container**:
   - Use the following command to start the container:

    ```bash
     docker run -it --rm \
         --runtime=nvidia --gpus all \
         -v $PWD:/workspace/neural_wbc \
         --entrypoint /bin/bash \
         --name neural_wbc \
         nvcr.io/nvidian/isaac-lab:IsaacLab-main-b120
    ```

4. **Set Up the Container**:
   - Navigate to the workspace and install dependencies:

     ```bash
     cd /workspace/neural_wbc
     ./install_deps.sh
     ```

You can now run scripts in headless mode by passing the `--headless` option.


# Acknowledgments

We would like to acknowledge the following projects where parts of the codes in this repo is derived from:

- [Mujoco Python Viewer](https://github.com/rohanpsingh/mujoco-python-viewer)
- [RSL RL](https://github.com/leggedrobotics/rsl_rl)
- [human2humanoid](https://github.com/LeCAR-Lab/human2humanoid)
- [Unitree Python SDK](https://github.com/unitreerobotics/unitree_sdk2_python)

[omnih2o_paper]: https://arxiv.org/abs/2406.08858
[hover_paper]: https://arxiv.org/abs/2410.21229

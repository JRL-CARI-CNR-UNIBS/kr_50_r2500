from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_moveit_rviz_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("kr_50_r2500", package_name="kr_50_r2500_moveit").to_moveit_configs()
    return generate_moveit_rviz_launch(moveit_config)

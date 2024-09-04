cmake_minimum_required(VERSION 3.8)
project(kr_50_r2500_description)

find_package(ament_cmake REQUIRED)

install(
    DIRECTORY
        config 
        launch 
        meshes
        urdf
    DESTINATION
        share/${PROJECT_NAME}
)

ament_package()
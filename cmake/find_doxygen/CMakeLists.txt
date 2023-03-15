cmake_minimum_required(VERSION 3.0)

project(MyProject)

find_package(Doxygen REQUIRED)

if(DOXYGEN_FOUND)
    message("Doxygen found: ${DOXYGEN_EXECUTABLE}")
else()
    message("Doxygen not found")
endif()

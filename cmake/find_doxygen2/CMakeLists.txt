cmake_minimum_required(VERSION 3.0.0)

project(LetMeFindDoxygen)

set(NEST_PATH /home/ejungwoo/nest)
set(CREATE_GIT_LOG ON)
set(BUILD_DOXYGEN_DOC ON)

find_package(Git)
if(CREATE_GIT_LOG)
  if(NOT GIT_FOUND)
    message(FATAL_ERROR "Git is needed to create git-log.")
    set(CREATE_GIT_LOG off)
  endif()
endif()

if(BUILD_DOXYGEN_DOC)
  find_package(Doxygen)
  #find_package(Doxygen REQUIRED)
endif()

#if(BUILD_DOXYGEN_DOC)
#  find_package(Doxygen)
#  if(NOT DOXYGEN_FOUND)
#    message(FATAL_ERROR "Doxygen is needed to build the documentation.")
#    set(BUILD_DOXYGEN_DOC off)
#  endif()
#endif()
#
#if(CREATE_GIT_LOG)
#  execute_process(COMMAND ${GIT_EXECUTABLE} rev-parse --abbrev-ref HEAD OUTPUT_VARIABLE NEST_GIT_BRANCH OUTPUT_STRIP_TRAILING_WHITESPACE WORKING_DIRECTORY ${NEST_PATH})
#  execute_process(COMMAND ${GIT_EXECUTABLE} rev-list --count ${NEST_GIT_BRANCH} OUTPUT_VARIABLE NEST_GIT_COMMIT_COUNT OUTPUT_STRIP_TRAILING_WHITESPACE WORKING_DIRECTORY ${NEST_PATH})
#  execute_process(COMMAND ${GIT_EXECUTABLE} rev-parse --short ${NEST_GIT_BRANCH} OUTPUT_VARIABLE NEST_GIT_HASH_SHORT OUTPUT_STRIP_TRAILING_WHITESPACE WORKING_DIRECTORY ${NEST_PATH})
#  set(NEST_VERSION "${NEST_GIT_BRANCH}.${NEST_GIT_COMMIT_COUNT}.${NEST_GIT_HASH_SHORT}")
#  set(NEST_VERSION_SHORT "${NEST_GIT_HASH_SHORT}")
#
#  execute_process(COMMAND ${GIT_EXECUTABLE} branch -l OUTPUT_VARIABLE NEST_GIT_BRANCH_LIST OUTPUT_STRIP_TRAILING_WHITESPACE WORKING_DIRECTORY ${NEST_PATH})
#  string(REPLACE "\n" ";" NEST_GIT_BRANCH_LIST "${NEST_GIT_BRANCH_LIST}")
#  string(REPLACE " " "" NEST_GIT_BRANCH_LIST "${NEST_GIT_BRANCH_LIST}")
#  string(REPLACE "*" "" NEST_GIT_BRANCH_LIST "${NEST_GIT_BRANCH_LIST}")
#
#  foreach(_branch ${NEST_GIT_BRANCH_LIST})
#    execute_process(COMMAND ${GIT_EXECUTABLE} log --reverse --oneline ${_branch} OUTPUT_VARIABLE NEST_GIT_BRANCH_LOGS)
#    list(APPEND NEST_GIT_BRANCH_LOG_LIST "__BRANCH__ ${_branch}")
#    foreach(_log ${NEST_GIT_BRANCH_LOGS})
#      list(APPEND NEST_GIT_BRANCH_LOG_LIST ${_log})
#    endforeach(_log)
#  endforeach(_branch)
#
#  string(REPLACE ";" "\n" NEST_GIT_BRANCH_LOG_LIST "${NEST_GIT_BRANCH_LOG_LIST}")
#
#  execute_process(COMMAND ${GIT_EXECUTABLE} rev-parse --abbrev-ref HEAD OUTPUT_VARIABLE GETDECODER_GIT_BRANCH OUTPUT_STRIP_TRAILING_WHITESPACE WORKING_DIRECTORY ${NEST_PATH}/GETDECODER)
#  execute_process(COMMAND ${GIT_EXECUTABLE} rev-list --count ${GETDECODER_GIT_BRANCH} OUTPUT_VARIABLE GETDECODER_GIT_COMMIT_COUNT OUTPUT_STRIP_TRAILING_WHITESPACE WORKING_DIRECTORY ${NEST_PATH}/GETDECODER)
#  set(GETDECODER_VERSION "${GETDECODER_GIT_BRANCH}.${GETDECODER_GIT_COMMIT_COUNT}")
#
#  execute_process(COMMAND ${GIT_EXECUTABLE} log --pretty=format:"%h %an %ar : %s" -1 OUTPUT_VARIABLE NEST_GIT_LOG_TEMP)
#  execute_process(COMMAND ${GIT_EXECUTABLE} status -s      OUTPUT_VARIABLE NEST_GIT_STATUS OUTPUT_STRIP_TRAILING_WHITESPACE)
#  execute_process(COMMAND ${GIT_EXECUTABLE} diff -U0 OUTPUT_VARIABLE NEST_GIT_DIFF OUTPUT_STRIP_TRAILING_WHITESPACE)
#  string(REPLACE \" "" NEST_GIT_LOG ${NEST_GIT_LOG_TEMP})
#
#  cmake_host_system_information(RESULT NEST_HOSTNAME QUERY HOSTNAME)
#
#  set(NEST_USERNAME $ENV{USER})
#
#  configure_file(${NEST_PATH}/log/NTCompiled.h.in  ${NEST_PATH}/log/NTCompiled.h @ONLY)
#  configure_file(${NEST_PATH}/log/NTCompiledStatus.log.in ${NEST_PATH}/log/NTCompiledStatus.log @ONLY)
#  configure_file(${NEST_PATH}/log/NTCompiledDiff.log.in ${NEST_PATH}/log/NTCompiledDiff.log @ONLY)
#  configure_file(${NEST_PATH}/log/NTBranchList.log.in ${NEST_PATH}/log/NTBranchList.log @ONLY)
#endif()
#
#if(BUILD_DOXYGEN_DOC)
#  configure_file(${NEST_PATH}/log/doxy.conf.in ${NEST_PATH}/log/doxy.conf @ONLY)
#  execute_process(COMMAND ${DOXYGEN_EXECUTABLE} ${NEST_PATH}/log/doxy.conf 
#                  WORKING_DIRECTORY ${NEST_PATH})
#endif()

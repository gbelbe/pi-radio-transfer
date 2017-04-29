# Install script for directory: /home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/python

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/raspi_decoder" TYPE FILE FILES
    "/home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/python/__init__.py"
    "/home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/python/psk_constellation_decoder.py"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/raspi_decoder" TYPE FILE FILES
    "/home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/build/python/__init__.pyc"
    "/home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/build/python/psk_constellation_decoder.pyc"
    "/home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/build/python/__init__.pyo"
    "/home/grembert/pi-radio-transfer/src/gnuradio/gr-raspi_decoder/build/python/psk_constellation_decoder.pyo"
    )
endif()


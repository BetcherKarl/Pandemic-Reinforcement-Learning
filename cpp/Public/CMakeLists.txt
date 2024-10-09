cmake_minimum_required(VERSION 3.29)
project(PandemicRLGame)

set(CMAKE_CXX_STANDARD 20)

include_directories(.)
include_directories(Public)

add_executable(PandemicRLGame
    Private/utils/board.cpp
    Private/utils/card.cpp
    Private/utils/city.cpp
    Private/utils/color.cpp
    Private/utils/player.cpp
    Private/PandemicGame.cpp
    Private/PandemicGameBoard.cpp
    Public/PandemicGame.h
    Public/PandemicGameBoard.h
    PandemicRLGame.cpp
    PandemicRLGame.h
        Private/utils/pandemic.h
        Private/utils/color.h
        Private/utils/City.h
        Private/utils/Card.h
        Private/utils/Player.h)

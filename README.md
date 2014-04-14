RobotMemory
===========

A library with code that helps robots save temporary memory

Currently in development for python, specifically with Myro and Scribbler robots.

Will possibly add C++ for other platforms later

Documentation
=====================

This API is meant to be used for storing robot memory.

It currently has modifier methods that support connecting to a robot, creating a plot, going forward, turning, and slight curves. The curves have an issue with going more than a half circle, correct orientation afterwards, and turning with curves(haven't even gone there yet...) 

Some of the get methods include retrieving nice location (not the index of the matrix), getting the current slope, and getting nearby cells. This area isn't my biggest concern because it is pretty self-explanitory, but I will continue to add to it if the main structure is finished.

Modifying methods
=================

| Name          | Purpose            | Parameters                                                                   |
|---------------|--------------------|------------------------------------------------------------------------------|
| `__init__`    | Basic constructor  | `self, [port, width, height, speed, scale, firstDirectionX, firstDirectionY]`|
| `start`       | Cretes the plot    | `[startx, starty]`                                                           |
| `goForward`   | Moves bot forward  | `duration`                                                                   |
| `turn`        | Turns the bot      | `degrees`                                                                    |
| `curve`       | Curves the bot     | `motorLeft, motorRight, duration`                                            |
-----------------------------------------------------------------------------------------------------------------------

Retrieving methods
==================

| Name            | Purpose                | Parameters                                                               |
|-----------------|------------------------|--------------------------------------------------------------------------|
| `getPosition`   | Gets the plot position | _none_                                                                   |
| `getSlope`      | Gets the plot slope    | _none_                                                                   |
| `getNearby`     | Gets the nearby cells  |`radius`                                                                  |
-----------------------------------------------------------------------------------------------------------------------

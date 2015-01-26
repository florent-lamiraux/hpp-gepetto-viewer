#!/usr/bin/env python

# Copyright (c) 2014 CNRS
# Author: Florent Lamiraux
#
# This file is part of hpp-gepetto-viewer.
# hpp-gepetto-viewer is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp-gepetto-viewer is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp-gepetto-viewer.  If not, see
# <http://www.gnu.org/licenses/>.

import os
import rospkg
from hpp.gepetto import ViewerFactory as Parent
from hpp.gepetto.manipulation import Viewer

## Viewer factory for manipulation.Viewer
#
#  Store commands to be sent to \c gepetto-viewer-server, create
#  clients on demand and send stored commands.
class ViewerFactory (Parent):
    ## Constructor
    #  \param problemSolver instance of class
    #         manipulation.problem_solver.ProblemSolver
    def __init__ (self, problemSolver) :
        Parent.__init__ (self, problemSolver)

    ##
    #  Do nothing for compatibility with parent class
    def buildRobotBodies (self):
        self.robotBodies = list ()

    def loadRobotModel (self, RobotType, robotName):
        self.robot.loadRobotModel (robotName, RobotType.rootJointType,
                                   RobotType.packageName,
                                   RobotType.modelName, RobotType.urdfSuffix,
                                   RobotType.srdfSuffix)
        self.buildRobotBodies ()
        self.loadUrdfInGUI (RobotType, robotName)

    def loadHumanoidModel (self, RobotType, robotName):
        self.robot.loadHumanoidModel (robotName, RobotType.rootJointType,
                                      RobotType.packageName,
                                      RobotType.modelName, RobotType.urdfSuffix,
                                      RobotType.srdfSuffix)
        self.buildRobotBodies ()
        self.loadUrdfInGUI (RobotType, robotName)

    def loadEnvironmentModel (self, EnvType, envName, guiOnly = False):
        if not guiOnly:
            self.robot.loadEnvironmentModel (EnvType.packageName, EnvType.urdfName,
                EnvType.urdfSuffix, EnvType.srdfSuffix, envName + "/")
        self.loadUrdfObjectsInGUI (EnvType, envName)
        self.computeObjectPosition ()

    def loadObjectModel (self, RobotType, robotName, guiOnly = False):
        if not guiOnly:
            self.robot.loadObjectModel (robotName, RobotType.rootJointType,
                                    RobotType.packageName, RobotType.urdfName,
                                    RobotType.urdfSuffix, RobotType.srdfSuffix)
        self.buildRobotBodies ()
        self.loadUrdfInGUI (RobotType, robotName)
        self.computeObjectPosition ()

    def buildCompositeRobot (self, robotNames):
        self.robot.buildCompositeRobot (robotNames)
        # build list of pairs (robotName, objectName)
        for j in self.robot.getAllJointNames ():
            # Guess robot name from joint name
            prefix = j.split ('/') [0]
            self.robotBodies.extend (map (lambda n: (j, prefix + '/', n),
                                          [self.robot.getLinkName (j), ]))

    def loadUrdfInGUI (self, RobotType, robotName):
        self.guiRequest.append ((Viewer.loadUrdfInGUI, locals ()));

    def loadUrdfObjectsInGUI (self, RobotType, robotName):
        self.guiRequest.append ((Viewer.loadUrdfObjectsInGUI, locals ()));

    ## Create a client to \c gepetto-viewer-server and send stored commands
    #
    def createRealClient (self, ViewerClass = Viewer, viewerClient = None):
        v = Parent.createRealClient (self, ViewerClass, viewerClient)
        v.robotBodies = self.robotBodies
        return v

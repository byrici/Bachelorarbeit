
"use strict";

let Reboot = require('./Reboot.js')
let MotorGains = require('./MotorGains.js')
let RegisterValues = require('./RegisterValues.js')
let RobotInfo = require('./RobotInfo.js')
let TorqueEnable = require('./TorqueEnable.js')
let OperatingModes = require('./OperatingModes.js')

module.exports = {
  Reboot: Reboot,
  MotorGains: MotorGains,
  RegisterValues: RegisterValues,
  RobotInfo: RobotInfo,
  TorqueEnable: TorqueEnable,
  OperatingModes: OperatingModes,
};


"use strict";

let SpatialDetection = require('./SpatialDetection.js');
let TrackedFeatures = require('./TrackedFeatures.js');
let TrackedFeature = require('./TrackedFeature.js');
let FFMPEGPacket = require('./FFMPEGPacket.js');
let SpatialDetectionArray = require('./SpatialDetectionArray.js');
let HandLandmark = require('./HandLandmark.js');
let HandLandmarkArray = require('./HandLandmarkArray.js');
let AutoFocusCtrl = require('./AutoFocusCtrl.js');
let ImuWithMagneticField = require('./ImuWithMagneticField.js');
let TrackDetection2DArray = require('./TrackDetection2DArray.js');
let ImageMarkerArray = require('./ImageMarkerArray.js');
let TrackDetection2D = require('./TrackDetection2D.js');
let ImageMarker = require('./ImageMarker.js');

module.exports = {
  SpatialDetection: SpatialDetection,
  TrackedFeatures: TrackedFeatures,
  TrackedFeature: TrackedFeature,
  FFMPEGPacket: FFMPEGPacket,
  SpatialDetectionArray: SpatialDetectionArray,
  HandLandmark: HandLandmark,
  HandLandmarkArray: HandLandmarkArray,
  AutoFocusCtrl: AutoFocusCtrl,
  ImuWithMagneticField: ImuWithMagneticField,
  TrackDetection2DArray: TrackDetection2DArray,
  ImageMarkerArray: ImageMarkerArray,
  TrackDetection2D: TrackDetection2D,
  ImageMarker: ImageMarker,
};

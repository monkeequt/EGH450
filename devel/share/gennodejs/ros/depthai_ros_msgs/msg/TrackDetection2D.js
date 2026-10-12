// Auto-generated. Do not edit!

// (in-package depthai_ros_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let vision_msgs = _finder('vision_msgs');

//-----------------------------------------------------------

class TrackDetection2D {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.results = null;
      this.bbox = null;
      this.is_tracking = null;
      this.tracking_id = null;
      this.tracking_age = null;
      this.tracking_status = null;
    }
    else {
      if (initObj.hasOwnProperty('results')) {
        this.results = initObj.results
      }
      else {
        this.results = [];
      }
      if (initObj.hasOwnProperty('bbox')) {
        this.bbox = initObj.bbox
      }
      else {
        this.bbox = new vision_msgs.msg.BoundingBox2D();
      }
      if (initObj.hasOwnProperty('is_tracking')) {
        this.is_tracking = initObj.is_tracking
      }
      else {
        this.is_tracking = false;
      }
      if (initObj.hasOwnProperty('tracking_id')) {
        this.tracking_id = initObj.tracking_id
      }
      else {
        this.tracking_id = '';
      }
      if (initObj.hasOwnProperty('tracking_age')) {
        this.tracking_age = initObj.tracking_age
      }
      else {
        this.tracking_age = 0;
      }
      if (initObj.hasOwnProperty('tracking_status')) {
        this.tracking_status = initObj.tracking_status
      }
      else {
        this.tracking_status = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type TrackDetection2D
    // Serialize message field [results]
    // Serialize the length for message field [results]
    bufferOffset = _serializer.uint32(obj.results.length, buffer, bufferOffset);
    obj.results.forEach((val) => {
      bufferOffset = vision_msgs.msg.ObjectHypothesisWithPose.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [bbox]
    bufferOffset = vision_msgs.msg.BoundingBox2D.serialize(obj.bbox, buffer, bufferOffset);
    // Serialize message field [is_tracking]
    bufferOffset = _serializer.bool(obj.is_tracking, buffer, bufferOffset);
    // Serialize message field [tracking_id]
    bufferOffset = _serializer.string(obj.tracking_id, buffer, bufferOffset);
    // Serialize message field [tracking_age]
    bufferOffset = _serializer.int32(obj.tracking_age, buffer, bufferOffset);
    // Serialize message field [tracking_status]
    bufferOffset = _serializer.int32(obj.tracking_status, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type TrackDetection2D
    let len;
    let data = new TrackDetection2D(null);
    // Deserialize message field [results]
    // Deserialize array length for message field [results]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.results = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.results[i] = vision_msgs.msg.ObjectHypothesisWithPose.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [bbox]
    data.bbox = vision_msgs.msg.BoundingBox2D.deserialize(buffer, bufferOffset);
    // Deserialize message field [is_tracking]
    data.is_tracking = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [tracking_id]
    data.tracking_id = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [tracking_age]
    data.tracking_age = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [tracking_status]
    data.tracking_status = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 360 * object.results.length;
    length += _getByteLength(object.tracking_id);
    return length + 57;
  }

  static datatype() {
    // Returns string type for a message object
    return 'depthai_ros_msgs/TrackDetection2D';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8f4e4ea4c4035ce11659980b4d3e8403';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    # Class probabilities
    vision_msgs/ObjectHypothesisWithPose[] results
    
    # 2D bounding box surrounding the object.
    vision_msgs/BoundingBox2D bbox
    
    # If true, this message contains object tracking information.
    bool is_tracking
    
    # ID used for consistency across multiple detection messages. This value will
    # likely differ from the id field set in each individual ObjectHypothesis.
    # If you set this field, be sure to also set is_tracking to True.
    string tracking_id
    
    # Age: number of frames the object is being tracked
    int32 tracking_age
    
    # Status of the tracking:
    # 0 = NEW -> the object is newly added.
    # 1 = TRACKED -> the object is being tracked.
    # 2 = LOST -> the object gets lost now. The object can be tracked again automatically (long term tracking) 
    #			  or by specifying detected object manually (short term and zero term tracking).
    # 3 = REMOVED -> the object is removed.
    int32 tracking_status
    
    ================================================================================
    MSG: vision_msgs/ObjectHypothesisWithPose
    # An object hypothesis that contains position information.
    
    # The unique numeric ID of object detected. To get additional information about
    #   this ID, such as its human-readable name, listeners should perform a lookup
    #   in a metadata database. See vision_msgs/VisionInfo.msg for more detail.
    int64 id
    
    # The probability or confidence value of the detected object. By convention,
    #   this value should lie in the range [0-1].
    float64 score
    
    # The 6D pose of the object hypothesis. This pose should be
    #   defined as the pose of some fixed reference point on the object, such a
    #   the geometric center of the bounding box or the center of mass of the
    #   object.
    # Note that this pose is not stamped; frame information can be defined by
    #   parent messages.
    # Also note that different classes predicted for the same input data may have
    #   different predicted 6D poses.
    geometry_msgs/PoseWithCovariance pose
    ================================================================================
    MSG: geometry_msgs/PoseWithCovariance
    # This represents a pose in free space with uncertainty.
    
    Pose pose
    
    # Row-major representation of the 6x6 covariance matrix
    # The orientation parameters use a fixed-axis representation.
    # In order, the parameters are:
    # (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)
    float64[36] covariance
    
    ================================================================================
    MSG: geometry_msgs/Pose
    # A representation of pose in free space, composed of position and orientation. 
    Point position
    Quaternion orientation
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    ================================================================================
    MSG: vision_msgs/BoundingBox2D
    # A 2D bounding box that can be rotated about its center.
    # All dimensions are in pixels, but represented using floating-point
    #   values to allow sub-pixel precision. If an exact pixel crop is required
    #   for a rotated bounding box, it can be calculated using Bresenham's line
    #   algorithm.
    
    # The 2D position (in pixels) and orientation of the bounding box center.
    geometry_msgs/Pose2D center
    
    # The size (in pixels) of the bounding box surrounding the object relative
    #   to the pose of its center.
    float64 size_x
    float64 size_y
    
    ================================================================================
    MSG: geometry_msgs/Pose2D
    # Deprecated
    # Please use the full 3D pose.
    
    # In general our recommendation is to use a full 3D representation of everything and for 2D specific applications make the appropriate projections into the plane for their calculations but optimally will preserve the 3D information during processing.
    
    # If we have parallel copies of 2D datatypes every UI and other pipeline will end up needing to have dual interfaces to plot everything. And you will end up with not being able to use 3D tools for 2D use cases even if they're completely valid, as you'd have to reimplement it with different inputs and outputs. It's not particularly hard to plot the 2D pose or compute the yaw error for the Pose message and there are already tools and libraries that can do this for you.
    
    
    # This expresses a position and orientation on a 2D manifold.
    
    float64 x
    float64 y
    float64 theta
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new TrackDetection2D(null);
    if (msg.results !== undefined) {
      resolved.results = new Array(msg.results.length);
      for (let i = 0; i < resolved.results.length; ++i) {
        resolved.results[i] = vision_msgs.msg.ObjectHypothesisWithPose.Resolve(msg.results[i]);
      }
    }
    else {
      resolved.results = []
    }

    if (msg.bbox !== undefined) {
      resolved.bbox = vision_msgs.msg.BoundingBox2D.Resolve(msg.bbox)
    }
    else {
      resolved.bbox = new vision_msgs.msg.BoundingBox2D()
    }

    if (msg.is_tracking !== undefined) {
      resolved.is_tracking = msg.is_tracking;
    }
    else {
      resolved.is_tracking = false
    }

    if (msg.tracking_id !== undefined) {
      resolved.tracking_id = msg.tracking_id;
    }
    else {
      resolved.tracking_id = ''
    }

    if (msg.tracking_age !== undefined) {
      resolved.tracking_age = msg.tracking_age;
    }
    else {
      resolved.tracking_age = 0
    }

    if (msg.tracking_status !== undefined) {
      resolved.tracking_status = msg.tracking_status;
    }
    else {
      resolved.tracking_status = 0
    }

    return resolved;
    }
};

module.exports = TrackDetection2D;

; Auto-generated. Do not edit!


(cl:in-package depthai_ros_msgs-msg)


;//! \htmlinclude TrackDetection2D.msg.html

(cl:defclass <TrackDetection2D> (roslisp-msg-protocol:ros-message)
  ((results
    :reader results
    :initarg :results
    :type (cl:vector vision_msgs-msg:ObjectHypothesisWithPose)
   :initform (cl:make-array 0 :element-type 'vision_msgs-msg:ObjectHypothesisWithPose :initial-element (cl:make-instance 'vision_msgs-msg:ObjectHypothesisWithPose)))
   (bbox
    :reader bbox
    :initarg :bbox
    :type vision_msgs-msg:BoundingBox2D
    :initform (cl:make-instance 'vision_msgs-msg:BoundingBox2D))
   (is_tracking
    :reader is_tracking
    :initarg :is_tracking
    :type cl:boolean
    :initform cl:nil)
   (tracking_id
    :reader tracking_id
    :initarg :tracking_id
    :type cl:string
    :initform "")
   (tracking_age
    :reader tracking_age
    :initarg :tracking_age
    :type cl:integer
    :initform 0)
   (tracking_status
    :reader tracking_status
    :initarg :tracking_status
    :type cl:integer
    :initform 0))
)

(cl:defclass TrackDetection2D (<TrackDetection2D>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TrackDetection2D>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TrackDetection2D)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name depthai_ros_msgs-msg:<TrackDetection2D> is deprecated: use depthai_ros_msgs-msg:TrackDetection2D instead.")))

(cl:ensure-generic-function 'results-val :lambda-list '(m))
(cl:defmethod results-val ((m <TrackDetection2D>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader depthai_ros_msgs-msg:results-val is deprecated.  Use depthai_ros_msgs-msg:results instead.")
  (results m))

(cl:ensure-generic-function 'bbox-val :lambda-list '(m))
(cl:defmethod bbox-val ((m <TrackDetection2D>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader depthai_ros_msgs-msg:bbox-val is deprecated.  Use depthai_ros_msgs-msg:bbox instead.")
  (bbox m))

(cl:ensure-generic-function 'is_tracking-val :lambda-list '(m))
(cl:defmethod is_tracking-val ((m <TrackDetection2D>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader depthai_ros_msgs-msg:is_tracking-val is deprecated.  Use depthai_ros_msgs-msg:is_tracking instead.")
  (is_tracking m))

(cl:ensure-generic-function 'tracking_id-val :lambda-list '(m))
(cl:defmethod tracking_id-val ((m <TrackDetection2D>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader depthai_ros_msgs-msg:tracking_id-val is deprecated.  Use depthai_ros_msgs-msg:tracking_id instead.")
  (tracking_id m))

(cl:ensure-generic-function 'tracking_age-val :lambda-list '(m))
(cl:defmethod tracking_age-val ((m <TrackDetection2D>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader depthai_ros_msgs-msg:tracking_age-val is deprecated.  Use depthai_ros_msgs-msg:tracking_age instead.")
  (tracking_age m))

(cl:ensure-generic-function 'tracking_status-val :lambda-list '(m))
(cl:defmethod tracking_status-val ((m <TrackDetection2D>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader depthai_ros_msgs-msg:tracking_status-val is deprecated.  Use depthai_ros_msgs-msg:tracking_status instead.")
  (tracking_status m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TrackDetection2D>) ostream)
  "Serializes a message object of type '<TrackDetection2D>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'results))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'results))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'bbox) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'is_tracking) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'tracking_id))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'tracking_id))
  (cl:let* ((signed (cl:slot-value msg 'tracking_age)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'tracking_status)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TrackDetection2D>) istream)
  "Deserializes a message object of type '<TrackDetection2D>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'results) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'results)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'vision_msgs-msg:ObjectHypothesisWithPose))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'bbox) istream)
    (cl:setf (cl:slot-value msg 'is_tracking) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'tracking_id) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'tracking_id) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'tracking_age) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'tracking_status) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TrackDetection2D>)))
  "Returns string type for a message object of type '<TrackDetection2D>"
  "depthai_ros_msgs/TrackDetection2D")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TrackDetection2D)))
  "Returns string type for a message object of type 'TrackDetection2D"
  "depthai_ros_msgs/TrackDetection2D")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TrackDetection2D>)))
  "Returns md5sum for a message object of type '<TrackDetection2D>"
  "8f4e4ea4c4035ce11659980b4d3e8403")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TrackDetection2D)))
  "Returns md5sum for a message object of type 'TrackDetection2D"
  "8f4e4ea4c4035ce11659980b4d3e8403")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TrackDetection2D>)))
  "Returns full string definition for message of type '<TrackDetection2D>"
  (cl:format cl:nil "~%# Class probabilities~%vision_msgs/ObjectHypothesisWithPose[] results~%~%# 2D bounding box surrounding the object.~%vision_msgs/BoundingBox2D bbox~%~%# If true, this message contains object tracking information.~%bool is_tracking~%~%# ID used for consistency across multiple detection messages. This value will~%# likely differ from the id field set in each individual ObjectHypothesis.~%# If you set this field, be sure to also set is_tracking to True.~%string tracking_id~%~%# Age: number of frames the object is being tracked~%int32 tracking_age~%~%# Status of the tracking:~%# 0 = NEW -> the object is newly added.~%# 1 = TRACKED -> the object is being tracked.~%# 2 = LOST -> the object gets lost now. The object can be tracked again automatically (long term tracking) ~%#			  or by specifying detected object manually (short term and zero term tracking).~%# 3 = REMOVED -> the object is removed.~%int32 tracking_status~%~%================================================================================~%MSG: vision_msgs/ObjectHypothesisWithPose~%# An object hypothesis that contains position information.~%~%# The unique numeric ID of object detected. To get additional information about~%#   this ID, such as its human-readable name, listeners should perform a lookup~%#   in a metadata database. See vision_msgs/VisionInfo.msg for more detail.~%int64 id~%~%# The probability or confidence value of the detected object. By convention,~%#   this value should lie in the range [0-1].~%float64 score~%~%# The 6D pose of the object hypothesis. This pose should be~%#   defined as the pose of some fixed reference point on the object, such a~%#   the geometric center of the bounding box or the center of mass of the~%#   object.~%# Note that this pose is not stamped; frame information can be defined by~%#   parent messages.~%# Also note that different classes predicted for the same input data may have~%#   different predicted 6D poses.~%geometry_msgs/PoseWithCovariance pose~%================================================================================~%MSG: geometry_msgs/PoseWithCovariance~%# This represents a pose in free space with uncertainty.~%~%Pose pose~%~%# Row-major representation of the 6x6 covariance matrix~%# The orientation parameters use a fixed-axis representation.~%# In order, the parameters are:~%# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)~%float64[36] covariance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: vision_msgs/BoundingBox2D~%# A 2D bounding box that can be rotated about its center.~%# All dimensions are in pixels, but represented using floating-point~%#   values to allow sub-pixel precision. If an exact pixel crop is required~%#   for a rotated bounding box, it can be calculated using Bresenham's line~%#   algorithm.~%~%# The 2D position (in pixels) and orientation of the bounding box center.~%geometry_msgs/Pose2D center~%~%# The size (in pixels) of the bounding box surrounding the object relative~%#   to the pose of its center.~%float64 size_x~%float64 size_y~%~%================================================================================~%MSG: geometry_msgs/Pose2D~%# Deprecated~%# Please use the full 3D pose.~%~%# In general our recommendation is to use a full 3D representation of everything and for 2D specific applications make the appropriate projections into the plane for their calculations but optimally will preserve the 3D information during processing.~%~%# If we have parallel copies of 2D datatypes every UI and other pipeline will end up needing to have dual interfaces to plot everything. And you will end up with not being able to use 3D tools for 2D use cases even if they're completely valid, as you'd have to reimplement it with different inputs and outputs. It's not particularly hard to plot the 2D pose or compute the yaw error for the Pose message and there are already tools and libraries that can do this for you.~%~%~%# This expresses a position and orientation on a 2D manifold.~%~%float64 x~%float64 y~%float64 theta~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TrackDetection2D)))
  "Returns full string definition for message of type 'TrackDetection2D"
  (cl:format cl:nil "~%# Class probabilities~%vision_msgs/ObjectHypothesisWithPose[] results~%~%# 2D bounding box surrounding the object.~%vision_msgs/BoundingBox2D bbox~%~%# If true, this message contains object tracking information.~%bool is_tracking~%~%# ID used for consistency across multiple detection messages. This value will~%# likely differ from the id field set in each individual ObjectHypothesis.~%# If you set this field, be sure to also set is_tracking to True.~%string tracking_id~%~%# Age: number of frames the object is being tracked~%int32 tracking_age~%~%# Status of the tracking:~%# 0 = NEW -> the object is newly added.~%# 1 = TRACKED -> the object is being tracked.~%# 2 = LOST -> the object gets lost now. The object can be tracked again automatically (long term tracking) ~%#			  or by specifying detected object manually (short term and zero term tracking).~%# 3 = REMOVED -> the object is removed.~%int32 tracking_status~%~%================================================================================~%MSG: vision_msgs/ObjectHypothesisWithPose~%# An object hypothesis that contains position information.~%~%# The unique numeric ID of object detected. To get additional information about~%#   this ID, such as its human-readable name, listeners should perform a lookup~%#   in a metadata database. See vision_msgs/VisionInfo.msg for more detail.~%int64 id~%~%# The probability or confidence value of the detected object. By convention,~%#   this value should lie in the range [0-1].~%float64 score~%~%# The 6D pose of the object hypothesis. This pose should be~%#   defined as the pose of some fixed reference point on the object, such a~%#   the geometric center of the bounding box or the center of mass of the~%#   object.~%# Note that this pose is not stamped; frame information can be defined by~%#   parent messages.~%# Also note that different classes predicted for the same input data may have~%#   different predicted 6D poses.~%geometry_msgs/PoseWithCovariance pose~%================================================================================~%MSG: geometry_msgs/PoseWithCovariance~%# This represents a pose in free space with uncertainty.~%~%Pose pose~%~%# Row-major representation of the 6x6 covariance matrix~%# The orientation parameters use a fixed-axis representation.~%# In order, the parameters are:~%# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)~%float64[36] covariance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: vision_msgs/BoundingBox2D~%# A 2D bounding box that can be rotated about its center.~%# All dimensions are in pixels, but represented using floating-point~%#   values to allow sub-pixel precision. If an exact pixel crop is required~%#   for a rotated bounding box, it can be calculated using Bresenham's line~%#   algorithm.~%~%# The 2D position (in pixels) and orientation of the bounding box center.~%geometry_msgs/Pose2D center~%~%# The size (in pixels) of the bounding box surrounding the object relative~%#   to the pose of its center.~%float64 size_x~%float64 size_y~%~%================================================================================~%MSG: geometry_msgs/Pose2D~%# Deprecated~%# Please use the full 3D pose.~%~%# In general our recommendation is to use a full 3D representation of everything and for 2D specific applications make the appropriate projections into the plane for their calculations but optimally will preserve the 3D information during processing.~%~%# If we have parallel copies of 2D datatypes every UI and other pipeline will end up needing to have dual interfaces to plot everything. And you will end up with not being able to use 3D tools for 2D use cases even if they're completely valid, as you'd have to reimplement it with different inputs and outputs. It's not particularly hard to plot the 2D pose or compute the yaw error for the Pose message and there are already tools and libraries that can do this for you.~%~%~%# This expresses a position and orientation on a 2D manifold.~%~%float64 x~%float64 y~%float64 theta~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TrackDetection2D>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'results) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'bbox))
     1
     4 (cl:length (cl:slot-value msg 'tracking_id))
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TrackDetection2D>))
  "Converts a ROS message object to a list"
  (cl:list 'TrackDetection2D
    (cl:cons ':results (results msg))
    (cl:cons ':bbox (bbox msg))
    (cl:cons ':is_tracking (is_tracking msg))
    (cl:cons ':tracking_id (tracking_id msg))
    (cl:cons ':tracking_age (tracking_age msg))
    (cl:cons ':tracking_status (tracking_status msg))
))

;; Auto-generated. Do not edit!


(when (boundp 'depthai_ros_msgs::TrackDetection2D)
  (if (not (find-package "DEPTHAI_ROS_MSGS"))
    (make-package "DEPTHAI_ROS_MSGS"))
  (shadow 'TrackDetection2D (find-package "DEPTHAI_ROS_MSGS")))
(unless (find-package "DEPTHAI_ROS_MSGS::TRACKDETECTION2D")
  (make-package "DEPTHAI_ROS_MSGS::TRACKDETECTION2D"))

(in-package "ROS")
;;//! \htmlinclude TrackDetection2D.msg.html
(if (not (find-package "VISION_MSGS"))
  (ros::roseus-add-msgs "vision_msgs"))


(defclass depthai_ros_msgs::TrackDetection2D
  :super ros::object
  :slots (_results _bbox _is_tracking _tracking_id _tracking_age _tracking_status ))

(defmethod depthai_ros_msgs::TrackDetection2D
  (:init
   (&key
    ((:results __results) ())
    ((:bbox __bbox) (instance vision_msgs::BoundingBox2D :init))
    ((:is_tracking __is_tracking) nil)
    ((:tracking_id __tracking_id) "")
    ((:tracking_age __tracking_age) 0)
    ((:tracking_status __tracking_status) 0)
    )
   (send-super :init)
   (setq _results __results)
   (setq _bbox __bbox)
   (setq _is_tracking __is_tracking)
   (setq _tracking_id (string __tracking_id))
   (setq _tracking_age (round __tracking_age))
   (setq _tracking_status (round __tracking_status))
   self)
  (:results
   (&rest __results)
   (if (keywordp (car __results))
       (send* _results __results)
     (progn
       (if __results (setq _results (car __results)))
       _results)))
  (:bbox
   (&rest __bbox)
   (if (keywordp (car __bbox))
       (send* _bbox __bbox)
     (progn
       (if __bbox (setq _bbox (car __bbox)))
       _bbox)))
  (:is_tracking
   (&optional (__is_tracking :null))
   (if (not (eq __is_tracking :null)) (setq _is_tracking __is_tracking)) _is_tracking)
  (:tracking_id
   (&optional __tracking_id)
   (if __tracking_id (setq _tracking_id __tracking_id)) _tracking_id)
  (:tracking_age
   (&optional __tracking_age)
   (if __tracking_age (setq _tracking_age __tracking_age)) _tracking_age)
  (:tracking_status
   (&optional __tracking_status)
   (if __tracking_status (setq _tracking_status __tracking_status)) _tracking_status)
  (:serialization-length
   ()
   (+
    ;; vision_msgs/ObjectHypothesisWithPose[] _results
    (apply #'+ (send-all _results :serialization-length)) 4
    ;; vision_msgs/BoundingBox2D _bbox
    (send _bbox :serialization-length)
    ;; bool _is_tracking
    1
    ;; string _tracking_id
    4 (length _tracking_id)
    ;; int32 _tracking_age
    4
    ;; int32 _tracking_status
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; vision_msgs/ObjectHypothesisWithPose[] _results
     (write-long (length _results) s)
     (dolist (elem _results)
       (send elem :serialize s)
       )
     ;; vision_msgs/BoundingBox2D _bbox
       (send _bbox :serialize s)
     ;; bool _is_tracking
       (if _is_tracking (write-byte -1 s) (write-byte 0 s))
     ;; string _tracking_id
       (write-long (length _tracking_id) s) (princ _tracking_id s)
     ;; int32 _tracking_age
       (write-long _tracking_age s)
     ;; int32 _tracking_status
       (write-long _tracking_status s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; vision_msgs/ObjectHypothesisWithPose[] _results
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _results (let (r) (dotimes (i n) (push (instance vision_msgs::ObjectHypothesisWithPose :init) r)) r))
     (dolist (elem- _results)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; vision_msgs/BoundingBox2D _bbox
     (send _bbox :deserialize buf ptr-) (incf ptr- (send _bbox :serialization-length))
   ;; bool _is_tracking
     (setq _is_tracking (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _tracking_id
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _tracking_id (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int32 _tracking_age
     (setq _tracking_age (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _tracking_status
     (setq _tracking_status (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get depthai_ros_msgs::TrackDetection2D :md5sum-) "8f4e4ea4c4035ce11659980b4d3e8403")
(setf (get depthai_ros_msgs::TrackDetection2D :datatype-) "depthai_ros_msgs/TrackDetection2D")
(setf (get depthai_ros_msgs::TrackDetection2D :definition-)
      "
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

")



(provide :depthai_ros_msgs/TrackDetection2D "8f4e4ea4c4035ce11659980b4d3e8403")



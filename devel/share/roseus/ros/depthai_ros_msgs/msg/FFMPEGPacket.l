;; Auto-generated. Do not edit!


(when (boundp 'depthai_ros_msgs::FFMPEGPacket)
  (if (not (find-package "DEPTHAI_ROS_MSGS"))
    (make-package "DEPTHAI_ROS_MSGS"))
  (shadow 'FFMPEGPacket (find-package "DEPTHAI_ROS_MSGS")))
(unless (find-package "DEPTHAI_ROS_MSGS::FFMPEGPACKET")
  (make-package "DEPTHAI_ROS_MSGS::FFMPEGPACKET"))

(in-package "ROS")
;;//! \htmlinclude FFMPEGPacket.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass depthai_ros_msgs::FFMPEGPacket
  :super ros::object
  :slots (_header _width _height _encoding _pts _flags _is_bigendian _data ))

(defmethod depthai_ros_msgs::FFMPEGPacket
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:width __width) 0)
    ((:height __height) 0)
    ((:encoding __encoding) "")
    ((:pts __pts) 0)
    ((:flags __flags) 0)
    ((:is_bigendian __is_bigendian) nil)
    ((:data __data) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _header __header)
   (setq _width (round __width))
   (setq _height (round __height))
   (setq _encoding (string __encoding))
   (setq _pts (round __pts))
   (setq _flags (round __flags))
   (setq _is_bigendian __is_bigendian)
   (setq _data __data)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:width
   (&optional __width)
   (if __width (setq _width __width)) _width)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:encoding
   (&optional __encoding)
   (if __encoding (setq _encoding __encoding)) _encoding)
  (:pts
   (&optional __pts)
   (if __pts (setq _pts __pts)) _pts)
  (:flags
   (&optional __flags)
   (if __flags (setq _flags __flags)) _flags)
  (:is_bigendian
   (&optional (__is_bigendian :null))
   (if (not (eq __is_bigendian :null)) (setq _is_bigendian __is_bigendian)) _is_bigendian)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int32 _width
    4
    ;; int32 _height
    4
    ;; string _encoding
    4 (length _encoding)
    ;; uint64 _pts
    8
    ;; uint8 _flags
    1
    ;; bool _is_bigendian
    1
    ;; uint8[] _data
    (* 1    (length _data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int32 _width
       (write-long _width s)
     ;; int32 _height
       (write-long _height s)
     ;; string _encoding
       (write-long (length _encoding) s) (princ _encoding s)
     ;; uint64 _pts
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _pts (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _pts) (= (length (_pts . bv)) 2)) ;; bignum
              (write-long (ash (elt (_pts . bv) 0) 0) s)
              (write-long (ash (elt (_pts . bv) 1) -1) s))
             ((and (class _pts) (= (length (_pts . bv)) 1)) ;; big1
              (write-long (elt (_pts . bv) 0) s)
              (write-long (if (>= _pts 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _pts s)(write-long (if (>= _pts 0) 0 #xffffffff) s)))
     ;; uint8 _flags
       (write-byte _flags s)
     ;; bool _is_bigendian
       (if _is_bigendian (write-byte -1 s) (write-byte 0 s))
     ;; uint8[] _data
     (write-long (length _data) s)
     (princ _data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int32 _width
     (setq _width (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _height
     (setq _height (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _encoding
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _encoding (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint64 _pts
     
#+(or :alpha :irix6 :x86_64)
      (setf _pts (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _pts (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; uint8 _flags
     (setq _flags (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; bool _is_bigendian
     (setq _is_bigendian (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; uint8[] _data
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _data (make-array n :element-type :char))
     (replace _data buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(setf (get depthai_ros_msgs::FFMPEGPacket :md5sum-) "4c1b25efca82fe4dd7addd520d7cc4b9")
(setf (get depthai_ros_msgs::FFMPEGPacket :datatype-) "depthai_ros_msgs/FFMPEGPacket")
(setf (get depthai_ros_msgs::FFMPEGPacket :definition-)
      "std_msgs/Header header
int32 width       # original image width
int32 height      # original image height
string encoding	  # encoding used
uint64 pts        # packet pts
uint8  flags      # packet flags
bool is_bigendian # true if machine stores in big endian format
uint8[] data      # ffmpeg compressed payload

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :depthai_ros_msgs/FFMPEGPacket "4c1b25efca82fe4dd7addd520d7cc4b9")



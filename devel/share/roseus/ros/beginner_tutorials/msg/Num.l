;; Auto-generated. Do not edit!


(when (boundp 'beginner_tutorials::Num)
  (if (not (find-package "BEGINNER_TUTORIALS"))
    (make-package "BEGINNER_TUTORIALS"))
  (shadow 'Num (find-package "BEGINNER_TUTORIALS")))
(unless (find-package "BEGINNER_TUTORIALS::NUM")
  (make-package "BEGINNER_TUTORIALS::NUM"))

(in-package "ROS")
;;//! \htmlinclude Num.msg.html


(defclass beginner_tutorials::Num
  :super ros::object
  :slots (_radius _velocity _direction ))

(defmethod beginner_tutorials::Num
  (:init
   (&key
    ((:radius __radius) 0.0)
    ((:velocity __velocity) 0.0)
    ((:direction __direction) 0.0)
    )
   (send-super :init)
   (setq _radius (float __radius))
   (setq _velocity (float __velocity))
   (setq _direction (float __direction))
   self)
  (:radius
   (&optional __radius)
   (if __radius (setq _radius __radius)) _radius)
  (:velocity
   (&optional __velocity)
   (if __velocity (setq _velocity __velocity)) _velocity)
  (:direction
   (&optional __direction)
   (if __direction (setq _direction __direction)) _direction)
  (:serialization-length
   ()
   (+
    ;; float32 _radius
    4
    ;; float32 _velocity
    4
    ;; float32 _direction
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _radius
       (sys::poke _radius (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _velocity
       (sys::poke _velocity (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _direction
       (sys::poke _direction (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _radius
     (setq _radius (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _velocity
     (setq _velocity (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _direction
     (setq _direction (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get beginner_tutorials::Num :md5sum-) "76bee1edb000cdff50e000ad59e430b2")
(setf (get beginner_tutorials::Num :datatype-) "beginner_tutorials/Num")
(setf (get beginner_tutorials::Num :definition-)
      "float32 radius
float32 velocity
float32 direction

")



(provide :beginner_tutorials/Num "76bee1edb000cdff50e000ad59e430b2")



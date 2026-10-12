#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/uavteam6/catkin_ws_G6/src/rqt_quaternion_view"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/uavteam6/catkin_ws_G6/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/uavteam6/catkin_ws_G6/install/lib/python3/dist-packages:/home/uavteam6/catkin_ws_G6/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/uavteam6/catkin_ws_G6/build" \
    "/usr/bin/python3" \
    "/home/uavteam6/catkin_ws_G6/src/rqt_quaternion_view/setup.py" \
     \
    build --build-base "/home/uavteam6/catkin_ws_G6/build/rqt_quaternion_view" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/uavteam6/catkin_ws_G6/install" --install-scripts="/home/uavteam6/catkin_ws_G6/install/bin"

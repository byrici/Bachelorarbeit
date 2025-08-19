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

echo_and_run cd "/my_project/src/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/my_project/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/my_project/install/lib/python3/dist-packages:/my_project/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/my_project/build" \
    "/usr/bin/python3" \
    "/my_project/src/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules/setup.py" \
    egg_info --egg-base /my_project/build/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules \
    build --build-base "/my_project/build/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/my_project/install" --install-scripts="/my_project/install/bin"

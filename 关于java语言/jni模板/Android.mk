LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := appdemo
LOCAL_SRC_FILES := appdemo.c
LOCAL_LDLIBS    += -llog
include $(BUILD_SHARED_LIBRARY)

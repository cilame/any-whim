#include "appdemo.h"

jstring Java_com_example_nihao_MainActivity_GetTest
  (JNIEnv * env, jobject obj){
	return (*env)->NewStringUTF(env, "hello world.");
}

jint Java_com_example_nihao_MainActivity_GetNumber
  (JNIEnv * env, jclass obj){
	return 123123333;
}

jfloat dynamic(){
	return 13.3f;
}

JNINativeMethod method[] = {
	{"GetNum", "()F", (void*)dynamic}
};

jint registerNativeMeth(JNIEnv *env){
	jclass clz = (*env)->FindClass(env, "com/example/nihao/MainActivity");
	if(((*env)->RegisterNatives(env, clz, method, sizeof(method)/sizeof(method[0])))<0){
		return -1;
	}
	return 0;
}

jint JNI_OnLoad(JavaVM* vm, void* reserved){
	JNIEnv *env;
	if ((*vm)->GetEnv(vm, (void**)&env, JNI_VERSION_1_4) != JNI_OK){
		return -1;
	}
	if (registerNativeMeth(env) != JNI_OK){
		return -1;
	}
	return JNI_VERSION_1_4;
}

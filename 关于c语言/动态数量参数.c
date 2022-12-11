#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#define ARG_T(T) T
#define ARG_N(_1,_2,_3,_4,_5,_6,_7,_8,_9,_10,_11,_12,_13,_14,_15,_16,_17,_18,_19,_20,N,...) N
#define ARG_N_HELP(...) ARG_T(ARG_N(__VA_ARGS__))
#define COUNT_ARG(...) ARG_N_HELP(__VA_ARGS__,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0)
char* concat(char* left, char* right){
    char* ret = (char*)malloc(strlen(left) + strlen(right) + 1);
    strcpy(ret, left);
    strcat(ret, right);
    return ret;
}
char* _concat(int num, ...){
    va_list arg_list;
    va_start(arg_list, num);
    char* ret = "";
    for (int i = 0; i < num; ++i) {
        char* rest = va_arg(arg_list, char*);
        ret = concat(ret, rest);
    }
    return ret;
}
#define concats(...) _concat(COUNT_ARG(__VA_ARGS__), __VA_ARGS__)

int main(int argc, char const *argv[]){
    printf("%s\n", concats("asdf", "ffff", "qoiwuye"));
    return 0;
}
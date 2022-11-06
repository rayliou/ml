#pragma once
#include <cstdint>
#include "DebugLogger.hpp"

class DebugStackFrames {

public:
    void log(int line=0){
        debugLogger.clear();
        debugLogger << "SF:";
        while(index_--> 0){
            debugLogger << frame_name_[index_];
            debugLogger << ":";
            //debugLogger << (  frame_ptr_[index_] - frame_ptr_[0]);
            debugLogger << (frame_ptr_[0] - frame_ptr_[index_]);
            debugLogger << ";";
        }
        debugLogger.log(line);
        clear();
    }
    void append(const char * name, void *ptr) {
        if ( index_ >= MAX_SIZE){
            return;
        }
        strncpy(frame_name_[index_], name, sizeof(frame_name_[0]));
        frame_ptr_[index_] = (uintptr_t )ptr;
        index_ ++;
    }
    void clear() {
        index_ = 0;
        memset(frame_name_, 0, sizeof(frame_name_));
        memset(frame_ptr_, 0, sizeof(frame_ptr_));
    }
    DebugStackFrames(){
        clear();
    }

    static void *memset(void *s, int c, std::size_t n) {
        unsigned char *ptr = (unsigned char *)s;
        while (n-- > 0) {
            *ptr++ = (unsigned char)c;
        }
        return s;
    }

    static char *strncpy(char *dest, const char *src, std::size_t n) {
        std::size_t i;
        for (i = 0; i < n && src[i] != '\0'; i++) {
            dest[i] = src[i];
        }
        for (; i < n; i++) {
            dest[i] = '\0';
        }
        return dest;
    }
private:
    static const int MAX_SIZE = 10;
    char frame_name_[MAX_SIZE][16];
    uintptr_t  frame_ptr_[MAX_SIZE];
    int index_ {0};
};
#if 0
extern DebugStackFrames debugStackFrames;
//Simple version
extern uintptr_t g_stack_main;
extern uintptr_t g_stack_last;
#endif

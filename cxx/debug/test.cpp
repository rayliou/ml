#include <cstdio>
#include "./include/Debug.hpp"

void debugPrint(const char * str1, const char *str2){
    printf("%s%s\n", str1,str2);
}
DebugLogger debugLogger;
DebugStackFrames debugStackFrames;

int main(int argc, char * argv[]){
    char x = 49;
    int64_t b = 88;
    debugLogger << "c";
    debugLogger << ":";
    debugLogger << -13;
    debugLogger << "  ";
    debugLogger << -2222.7895;
    debugLogger << "  ";
    debugLogger << -3.9e-32;
    debugLogger << "  ";
    debugLogger << -139999999999;
    debugLogger << "  ";
    debugLogger.setBase(16);
    debugLogger << 0x999999;
    debugLogger.print(__LINE__, __FILE__);
    debugStackFrames.append("x", &x);
    debugStackFrames.append("b", &b);
    debugStackFrames.log();
    return 0;

}

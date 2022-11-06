#pragma once
//#include <stdio.h>
#include <cstdint>
#include <type_traits>


void debugPrint(const char * str1, const char *str2);

class OStreamBuffer {
private:
    static const int bufferSize = 8;
    char buffer[bufferSize];
    //char *buffer {nullptr};
    int index = 0;
    int base = 10;

    template <typename T>
    void appendInteger(T value) {
        if (index >= bufferSize) return;

        bool isNegative = std::is_signed<T>::value && value < 0;
        if (isNegative) {
            value = -value;
        }

        char temp[64];
        size_t tempIndex = 0;

        do {
            T digit = value % base;
            temp[tempIndex++] = (digit < 10) ? '0' + digit : 'A' + digit - 10;
            value /= base;
        } while (value && (tempIndex < sizeof(temp)));

        if (isNegative) {
            temp[tempIndex++] = '-';
        }

        for (size_t i = 0; i < tempIndex / 2; ++i) {
            char tmp = temp[i];
            temp[i] = temp[tempIndex - i - 1];
            temp[tempIndex - i - 1] = tmp;
        }

        for (size_t i = 0; i < tempIndex && index < bufferSize; ++i) {
            buffer[index++] = temp[i];
        }

        buffer[index] = '\0';
    }

    void appendFloat(float value, int precision = 4) {
        if (index >= bufferSize) return;
        if (value < 0.0f) {
            buffer[index++] = '-';
            value = -value;
        }
        int exponent = 0;
        while (value >= 10.0f) {
            value /= 10.0f;
            ++exponent;
        }
        while (value > 0.0f && value < 1.0f) {
            value *= 10.0f;
            --exponent;
        }
        int intValue = static_cast<int>(value);
        appendInteger(intValue);
        if (index >= bufferSize) return;
        buffer[index++] = '.';
        float fraction = value - intValue;
        for (int i = 0; i < precision; ++i) {
            fraction *= 10;
            intValue = static_cast<int>(fraction);
            fraction -= intValue;
            if (index < bufferSize) {
                buffer[index++] = '0' + intValue;
            }
        }
        if (index >= bufferSize) return;
        buffer[index++] = 'E';
        appendInteger(exponent);
        buffer[index] = '\0';
    }

public:
    OStreamBuffer(){
        buffer[0] = '\0';
    }
    ~OStreamBuffer(){ }

 template <typename T>
    OStreamBuffer& operator<<(const T& value) {
        static_assert(std::is_integral<T>::value, "Only integral types are supported");
        appendInteger(value);
        return *this;
    }
template <typename T>
    OStreamBuffer& operator<<(T* ptr) {
        auto old_base  = base;
        base  = 16;
        *this << ((uint64_t)(uintptr_t)ptr);
        base = old_base;
        *this << "_P";
        return *this;
    }

    OStreamBuffer& operator<<(const char* value) {
        while (*value && index < bufferSize) {
            buffer[index++] = *value++;
        }
        buffer[index] = '\0';
        return *this;
    }


    OStreamBuffer& operator<<(bool value) {
        *this << (value ? "T" : "F");
        return *this;
    }

    OStreamBuffer& operator<<(const float value) {
        appendFloat(value);
        return *this;
    }
    OStreamBuffer& operator<<(const double value) {
        appendFloat((float)value);
        return *this;
    }
    OStreamBuffer& clear(){
        index = 0;
        *buffer = '\0';
        int n = bufferSize;
        char * p = buffer;
        while(n-->0){ *p++ = '\0'; }
        return *this;
    }
    OStreamBuffer& setBase(int newBase) {
        if (newBase == 10 || newBase == 16) {
            base = newBase;
        }
        return *this;
    }

    const char* c_str() const {
        return buffer;
    }
};
class DebugLogger {
public:
    DebugLogger (){ clear(); }
    void print(int line =0, const char * file=NULL){ log(line,file); }
    void log(int line =0, const char * file=NULL){
        pre_.clear();
        if (NULL != file){
            pre_ << file;
        }
        if (line != 0){
            pre_ << ":";
            pre_ << line;
        }
        pre_ << " ";
        debugPrint(pre_.c_str(), body_.c_str());
        clear();
    }
    void clear() {
        pre_.clear();
        body_.clear();
    }
    DebugLogger& setBase(int base) {body_.setBase(base); return *this;}
 template <typename T>
 DebugLogger& operator<<(const T& value) {
        body_ << value;
        return *this;
    }

private:
    OStreamBuffer pre_;
    OStreamBuffer body_;
};
extern DebugLogger debugLogger;

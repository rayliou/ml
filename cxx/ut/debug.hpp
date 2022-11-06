
#ifndef __DEBUG__HPP__
#define __DEBUG__HPP__
#include <cstdio>
#ifdef USE_KNOWLES
#include "fr32_utils.h"
#endif //USE_KNOWLES

extern bool enable_debug_log;
extern int processed_frames;
template<typename T> 
inline
float cfloat_to_float(T v) { return v; }
#ifdef USE_KNOWLES
template<> inline float cfloat_to_float(fr32 v) { return afloat_to_float(v); }
#endif //USE_KNOWLES

template<typename T> 
inline
void print_element(T v, float scale, float offset){
    if(!enable_debug_log){ return; }
    v *= scale;
    v += offset;
    printf("\t%d",v);
}

template<> inline
void print_element(float v, float scale, float offset){
    if(!enable_debug_log){ return; }
    v *= scale;
    v += offset;
    printf("\t%e",v);
}

#ifdef __REAL_CUSTOM__
template<> inline
void print_element(fluent::Real_Custom v, float scale, float offset){
    print_element((float)v, scale, offset);
}
#endif //__REAL_CUSTOM__
#ifdef USE_KNOWLES
template<> inline
void print_element(fr32 vfr32, float scale, float offset){
    float v = afloat_to_float(vfr32);
    print_element(v, scale, offset);
}
#endif //USE_KNOWLES

template<typename T> inline void debugPrint(const fluent::span<T> &s, const char *name = "", float scale=1, float offset=0.0, int max_cnt = 80, int line_element_count = 8) {
    if(!enable_debug_log){ return; }
    printf("\n[%d:%s] %s size=%lu scale=%f, offset=%f",processed_frames, name, "Output: ", s.size(), scale,offset);
    int cnt = 0;
    float min {0};
    float max {0};
    for(auto &f: s) {
        if(cnt < max_cnt) {
            if (cnt % line_element_count == 0) {
                printf("\n[%d:%s] ",processed_frames, name);
            }
            print_element(f,scale,offset);
        }
        auto v = cfloat_to_float(f);
        max = v>max? v: max;
        min = v < min? v: min;
        cnt++;
    }
    max = max *scale+offset;
    min = min *scale+offset;
    printf("\n[%d:%s] Max: %e, Min: %e\n",processed_frames, name, max, min);
}

template<typename T> inline void debugPrint(const T *src, size_t size, const char *name = "", float scale=1.0, float offset=0.0, int max_cnt = 80, int line_element_count = 8) {
    fluent::span<T> s = fluent::make_span<T>((T*)src, (T*)src+size);
    debugPrint(s, name, scale, offset, max_cnt,line_element_count);
}
template<typename T> inline void debugPrint(const fluent::Matrix<T> &m,const char *name = "", float scale=1.0, float offset=0.0, int max_cnt = 80, int line_element_count = 8) {
    fluent::span<T> s = fluent::make_span<T>((T*)m.p_data, (T*)m.p_data+m.size());
    debugPrint(s, name, scale, offset, max_cnt,line_element_count);
}
#if 0
namespace fluent
{
	//inline 
        void log_activations(const char* model_name, const char* layer_name, Matrix<float> mtx, int16_t data_shift){
        char str[1024];
        snprintf(str, 1024, "%s_%s",model_name ,layer_name);
        debugPrint(mtx, str);

    }
    //inline 
 	void log_activations(const char* model_name, const char* layer_name, Matrix<int8_t> mtx, int16_t data_shift){
        char str[1024];
        snprintf(str, 1024, "%s_%s",model_name ,layer_name);
        debugPrint(mtx, str);

    }
	//void log_activations(const char* model_name, const char* layer_name, Matrix<qf32_t> mtx, int16_t data_shift);
	void log_activations(const char* model_name, const char* layer_name, Matrix<short> mtx, int16_t data_shift);
	//void log_activations(const char* model_name, const char* layer_name, Matrix<int64_t> mtx, int16_t data_shift);
}
#endif

#endif //__DEBUG__HPP__

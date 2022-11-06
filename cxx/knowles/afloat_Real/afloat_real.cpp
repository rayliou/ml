#include <cstdio>
#include <limits>
#include "fr32_utils.h"
#include "AScalar.h"
// https://fluentai.atlassian.net/jira/software/c/projects/SWE/boards/40?modal=detail&selectedIssue=SWE-1171&assignee=637649482acfad92d7affbfe
#include "real_custom.hpp"

template<class T>
void debugLog(const char* label, T data) {
    return;
    int bit_count  = sizeof(data) *8;
    char buffer[65];
    for (int i = bit_count - 1; i >= 0; i--) {
        buffer[i] = (data & 1) ? '1' : '0';
        data >>= 1;
    }
    buffer[bit_count] = '\0';
    printf("%s:\t%s\n", label,buffer);
}



_AI float afloat_to_float_with_rounding(const fr32 fr, int round_bit = 2) {
    if(round_bit <= 0){
        return afloat_to_float(fr);
    }
    if ( eq_fr(FR32_MAX_AFLOAT, fr) || eq_fr(FR32_MIN_AFLOAT, fr)){
        return afloat_to_float(fr);
    }
    uint32_t u32  = move_ar_fr(fr);
    uint32_t sign = u32 & 0x80000000;
    uint32_t exp  = u32 & 0x7e000000;
    uint32_t mant = u32 & 0x01ffffff;
    auto mant_old = mant;
    auto exp_old = exp;
    uint32_t mask = (1 << (round_bit - 1))
            | (1 << (round_bit - 2));
    if (mant & mask) {
        mant += (1 << round_bit);
        mant &= ~((1 << round_bit) - 1);
        if (mant & 0x02000000) {
            if (0x7e000000 == exp){
                return sign? afloat_to_float(FR32_MIN_AFLOAT) : afloat_to_float(FR32_MAX_AFLOAT);
            }
            mant >>= 1;
            exp += (1 << 25);
        }
    }

    debugLog("u32", u32);
    debugLog("sign", sign);
    debugLog("exp_old", exp_old);
    debugLog("exp    ", exp);
    debugLog("mant_old", mant_old);
    debugLog("mant    ", mant);

    uint64_t u64  = ((uint64_t) sign << 32) | ((uint64_t) mant << 27);
    if (exp | mant)
        u64 |= (uint64_t) ((exp >> 25) + 991) << 52;
    double result_double = *(double*) &u64;
    return static_cast<float>(result_double);
}

class TestAdd {
public:
    TestAdd(int round_bit=2):round_bit(round_bit){ }
    void run(bool log_detail=true){
            printf("\nTest test_add with round_bit=%d\n",round_bit);
            double base_list[] = {afloat_to_double(FR32_MAX_AFLOAT) - 400,
                                  afloat_to_double(FR32_MIN_AFLOAT) + 400};
            for (auto base : base_list) {
                for (auto f = -fMax; f <= fMax; f += step) {
                    run(base,f,log_detail);
                }
            }
            float avg_diff = sum_diff / diff_count;
            float percent_diff_not_equal = (float(diff_count) / float(total_count)) * 100.0f;
            printf("\nTEST add: Not_Equal_vs_Real: %f%% ",percent_diff_not_equal);
            printf("total_count=%d diff_count=%d ", total_count, diff_count);
            printf("max_diff=%f, min_diff=%f, avg_diff=%f\n",max_diff, min_diff, avg_diff);
            double avg_PercentDiffReal = sum_PercentDiffReal / diff_count;
            double avg_PercentDiffAFloat = sum_PercentDiffAFloat / diff_count;
            printf("\nMax PercentDiffReal: %f%%, Min PercentDiffReal: %f%%, Avg PercentDiffReal: %f%%",
                   max_PercentDiffReal, min_PercentDiffReal, avg_PercentDiffReal);
            printf("\nMax PercentDiffAFloat: %f%%, Min PercentDiffAFloat: %f%%, Avg PercentDiffAFloat: %f%%\n",
                   max_PercentDiffAFloat, min_PercentDiffAFloat, avg_PercentDiffAFloat);
        }
        void run(double base, double f, bool log_detail=true) {
//            printf("%s(base=%f,f=%f)\n", __PRETTY_FUNCTION__ , base, f);
            total_count++;
            auto sum_expected = base + f;
            auto sum_afloat = AScalar(base) + AScalar(f);
            float sum_real = Real(base) + Real(f);
            auto sum_afloat_f = afloat_to_float_with_rounding(sum_afloat, round_bit);
            auto sum_afloat_dbl = afloat_to_double(sum_afloat);
            auto diff = sum_afloat_f - sum_real;
#if 1
            if(log_detail){
                printf("\nsum_afloat:          to_float=%+f"
                       "\n                    to_double=%+f"
                       "\nafloat_to_float_with_rounding=%+f\n",
                       afloat_to_float(sum_afloat),
                       afloat_to_double(sum_afloat),
                       sum_afloat_f
                       );
            }
#endif
            if (diff == 0.0f) {
                if(log_detail){
                    printf("%s", ".");
                }
            } else {
                diff_count++;
                sum_diff += Real::abs(diff);
                if (diff > max_diff) {
                    max_diff = diff;
                }
                if (diff < min_diff) {
                    min_diff = diff;
                }
                double percent_diff_real = (sum_real - sum_expected) / base * 100;
                double percent_diff_afloat =(sum_afloat_f - sum_expected) / base * 100;
                double percent_diff_afloat_dbl =(sum_afloat_dbl - sum_expected) / base * 100;
                // Update PercentDiffReal statistics
                if (percent_diff_real > max_PercentDiffReal) max_PercentDiffReal = percent_diff_real;
                if (percent_diff_real < min_PercentDiffReal) min_PercentDiffReal = percent_diff_real;
                sum_PercentDiffReal += percent_diff_real;
                // Update PercentDiffAFloat statistics
                if (percent_diff_afloat > max_PercentDiffAFloat) max_PercentDiffAFloat = percent_diff_afloat;
                if (percent_diff_afloat < min_PercentDiffAFloat) min_PercentDiffAFloat = percent_diff_afloat;
                sum_PercentDiffAFloat += percent_diff_afloat;
                if(log_detail){
                    printf("\nDiff=%f (base+f): (%f) +(%f)\n", diff,base,f);
                    printf("\nExpected         =%+f%% sum_expected=%+f", 0.0,sum_expected);
                    printf("\nPercentDiffAFloat=%+f%% sum_afloat  =%+f",  percent_diff_afloat,sum_afloat_f);
                    printf("\nPercentDiffReal  =%+f%% sum_real    =%+f",  percent_diff_real, sum_real);
                    puts("\n");
                }
            }
        }
private:
    int round_bit = 2;
    double fMax = 10000.0f;
    double step = 0.5;
    int total_count = 0;
    int diff_count = 0;
    double max_diff = 0.0;
    double min_diff = std::numeric_limits<double>::max();
    double sum_diff = 0.0;
    // Initialize variables
    double max_PercentDiffReal = std::numeric_limits<double>::lowest();
    double min_PercentDiffReal = std::numeric_limits<double>::max();
    double sum_PercentDiffReal = 0.0;
    double max_PercentDiffAFloat = std::numeric_limits<double>::lowest();
    double min_PercentDiffAFloat = std::numeric_limits<double>::max();
    double sum_PercentDiffAFloat = 0.0;
};


void test_sub() {
    AScalar max_s {FR32_MAX_AFLOAT};
    float a  = max_s.to_float() -3;
    printf("%-30s %-30s %-30s %-30s %-30s\n","Data", "Expected", "afloat" ,"Reeal", "float");
    printf("%-30s %-30f %-30f %-30f %-30f\n","Base", static_cast<double>(a), a, a, a);

    //float b  = 4294956800.0;
    float b  = 10000.0;
    auto expected = static_cast<double>(a) - static_cast<double>(b);
    auto diff_a = afloat_to_float_with_rounding(AScalar(a) - AScalar(b));
    auto diff_r = float(Real(a) - Real(b));
    auto diff_f = a-b;

    printf("-%-29f %-30f %-30f %-30f %-30f\n", b, expected, diff_a, diff_r, diff_f);
    printf("base-diff         %-30f %-30f %-30f %-30f\n", expected - expected, diff_a - expected, diff_r - expected, diff_f - expected);
}



int main() {
#if 0
    for(auto round_bit=1; round_bit<=4;round_bit++){
        TestAdd testAdd(round_bit);
        testAdd.run(false);
    }
    return 0;
#endif
    TestAdd testAdd;
    //testAdd.run(true); return 0;
// Diff=256.000000 (base+f): (4294966832.000000) +(-9397.500000)
    testAdd.run(4294966832.0,-9397.50 ); return 0;
// Diff=-256.000000 f=-5783.500000, base=4294966832.000000
    testAdd.run(4294966832.000000,-5783.500000);// return 0;
//Diff=256.000000 f=9904.000000, base=-4294966832.000000
    testAdd.run(-4294966832.000000,9904.000000); return 0;
// Diff=-256.000000, PercentDiffReal=-0.000004%, PercentDiffAFloat=0.000002%,
// f=9090.000000, base=-4294966832.000000, sum_expected=-4294957742.000000, sum_real=-4294957568.000000,
// sum_afloat=-4294957824.000000
    testAdd.run(-4294966832.000000,9090); return 0;
//    test_sub(); return 0;
    Real a(1.0), b(0.0001);
    Real sum = a + b;
    Real difference = a - b;
    Real product = a * b;
    Real quotient = a / b;
    printf("sizeof quotient is %d\n",sizeof(quotient ));

    sum.print();
    difference.print();
    product.print();
    quotient.print();
    AScalar max_s {FR32_MAX_AFLOAT}; //4294967040
    AScalar min_s {FR32_MIN_AFLOAT};
    auto max_f = max_s.to_float();
    auto min_f = min_s.to_float();
    printf("Afloat: maxPositiveValue=%f min=%f\n", max_f, min_f);
    //minPositiveValue
    AScalar s {0.001};
    AScalar minPositiveValue {s};
    while(s > FR32_ZERO){
        minPositiveValue = s;
        s/= FR32_TWO;
    }
    printf("Afloat: minPositiveValue=%g\n", minPositiveValue.to_float());
    // epsilon //3.05176e-08
    s = FR32_ONE;
    AScalar epsilon{minPositiveValue};
    do {
        epsilon *= FR32_TWO;
        s =  epsilon + FR32_ONE;
    }while(s == FR32_ONE);
    printf("Afloat: epsilon=%g\n", epsilon.to_float());

    return 0;
}


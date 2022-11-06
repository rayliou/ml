#pragma once

//#define __UT__WITH_MAIN__
#include <cstdio>

#define REQUIRE(cond) if (!(cond)) {\
    __ut_ret__ = false; printf("[REQUIRE] %s:%d: Failed: %s\n", __FILE__, __LINE__, #cond); return;\
}

#define CHECK(cond) if (!(cond)) {\
    __ut_ret__ = false; printf("[CHECK]%s:%d: Failed: %s\n", __FILE__, __LINE__, #cond);\
}

#define TEST_CASE(name) TEST_CASE_(name, __COUNTER__)
#define TEST_CASE_(name, counter) TEST_CASE__(name, counter)

//Insert the test case by the constructor of the global variable  test_instance_##counter
#define TEST_CASE__(name, counter) \
    void test_func_##counter(bool &);\
    struct test_##counter##_t {\
        test_##counter##_t() {\
            Tests::add_test(test_func_##counter, name);\
        }\
    } test_instance_##counter;\
    void test_func_##counter(bool &__ut_ret__)

#ifndef MAX_CASE_NUM 
#define MAX_CASE_NUM  2048
#endif

class Tests {
public:
    typedef void (*test_func)(bool &__ut_ret__);
    struct test_t {
        test_func function;
        const char* name;
    };

    static void add_test(test_func function, const char* name) {
        test_t test = { function, name };
        tests[num_tests++] = test;
    }

    static void run_tests(const char* filter = "*") {
            for (int i = 0; i < num_tests; ++i) {
                bool __ut_ret__ {true};
                if(match(filter, tests[i].name)) {
                    tests[i].function(__ut_ret__);
                    printf("%s: %s\n", tests[i].name, (__ut_ret__?"Passed":"Failed"));
                }
            }
        }

private:
   static bool match(const char* pattern, const char* str) {
        // Skip over any leading '*'
        while (*pattern == '*') {
            ++pattern;
            if (*pattern == '\0') {
                // If pattern is only '*', it matches everything
                return true;
            }
        }
        const char* str_start = str;
        while (*str != '\0') {
            if (match_here(pattern, str)) {
                return true;
            }
            ++str;
        }
        return match_here(pattern, str_start);
    }

    static bool match_here(const char* pattern, const char* str) {
        // At the end of the pattern
        if (*pattern == '\0') {
            return true;
        }
        // Match a single character or '*'
        if (*pattern == '?' || *pattern == *str) {
            return match_here(pattern + 1, str + 1);
        }
        // Match zero or more characters until the rest of the pattern matches
        if (*pattern == '*') {
            return match_here(pattern + 1, str) || (*str != '\0' && match_here(pattern, str + 1));
        }
        return false;
    }
private:
    static test_t tests[MAX_CASE_NUM];
    static int num_tests;
};

Tests::test_t Tests::tests[MAX_CASE_NUM];
int Tests::num_tests = 0;

#ifdef __UT__WITH_MAIN__
int main(int argc, char* argv[]) {
    const char* filter = "*";
    if (argc > 1) {
        filter = argv[1];
    }
    Tests::run_tests(filter);
    return 0;
}
#endif

TEST_CASE("My first test") {
    REQUIRE(1 == 1);
    CHECK(1 != 1);
    CHECK(2 == 2);
}

//FYI: What common algorithms are used for C's rand()? : 
//  https://stackoverflow.com/questions/1026327/what-common-algorithms-are-used-for-cs-rand
//  Use a faster old version glibc rand number generator
//
//  Set seed as 1678717964 which is the seconds since 1970-01-01 00:00:00 UTC to  Mon 13 Mar 2023 10:32:44 AM EDT
static unsigned int rnd_seed_next = 1678717964;
static const auto FLUENTAI_RAND_MAX = (unsigned long long)(1UL << 31);
inline int rand_r (/*unsigned int *seed*/)
{
  int result;

  rnd_seed_next *= 1103515245;
  rnd_seed_next += 12345;
  result = (unsigned int) (rnd_seed_next / 65536) % 2048;

  rnd_seed_next *= 1103515245;
  rnd_seed_next += 12345;
  result <<= 10;
  result ^= (unsigned int) (rnd_seed_next / 65536) % 1024;

  rnd_seed_next *= 1103515245;
  rnd_seed_next += 12345;
  result <<= 10;
  result ^= (unsigned int) (rnd_seed_next / 65536) % 1024;
  return result;
}

#pragma once
#include <cstdio>
// https://fluentai.atlassian.net/jira/software/c/projects/SWE/boards/40?modal=detail&selectedIssue=SWE-1171&assignee=637649482acfad92d7affbfe


class Real {
public:
    Real(double val) : value_(val) { handleValueLimits(value_); }
    Real(const Real& other) : value_(other.value_) {}
    // Unary operator -
    Real operator-() const { return Real(-value_); }
    // Assignment operator
    Real& operator=(const Real& other) {
        if (this != &other) {
            value_ = other.value_;
        }
        return *this;
    }
    // Add
    Real operator+(const Real &other) const {
        auto sum = value_ + other.value_;
        auto bigger = abs(value_) > abs(other.value_) ? value_ : other.value_;
        auto smaller = abs(value_) < abs(other.value_) ? value_ : other.value_;
        if (abs(smaller) / abs(bigger) < epsilon_) {
            return Real(bigger);
        }
//        printf("%d:%s:sum=%f=%f + %f\n", __LINE__, __PRETTY_FUNCTION__,sum, this->value_, other.value_);
        return Real(sum);
    }
    // Subtract
    Real operator-(const Real &other) const {
        return *this + (-other);
    }
    // Multiply
    Real operator*(const Real &other) const {
        auto product = value_ * other.value_;
        return Real(product);
    }
    // Divide
    Real operator/(const Real &other) const {
        if (other.value_ == 0.0f) {
            return Real(0.0f);
        }
        auto quotient = value_ / other.value_;
        return Real(quotient);
    }
    Real& operator+=(const Real &other) { *this = *this + other; return *this; }
    Real& operator-=(const Real &other) { *this = *this - other; return *this; }
    Real& operator*=(const Real &other) { *this = *this * other; return *this; }
    Real& operator/=(const Real &other) { *this = *this / other; return *this; }
    // Automatic conversion to float (with truncation)
    operator float() const {
        auto truncatedValue = value_;
        handleValueLimits(truncatedValue);
        return (float)truncatedValue;
    }
    void handleValueLimits(double &val) const {
//        printf("Start %s:%f\n", __PRETTY_FUNCTION__ ,val);
        if (val > maxPositiveValue_) {
            val = maxPositiveValue_;
        } else if (val < maxNegativeValue_) {
            val = maxNegativeValue_;
        } else if (abs(val) < minPositiveValue_) {
            val = 0.0f;
        }
//        printf("End %s:%f\n", __PRETTY_FUNCTION__ ,val);
    }
    // Print value
    void print() const {
        auto truncatedValue = value_;
        handleValueLimits(truncatedValue);
        printf("%g\n", truncatedValue);
    }
public:
    constexpr static double epsilon_ = 3.05176e-08;  // Epsilon for numerical precision
    constexpr static double maxPositiveValue_ = 4294967040.0f;  // Max positive value
    constexpr static double minPositiveValue_ = 2.38419e-10;  // Min positive value
    constexpr static double maxNegativeValue_ = -4294967040.0f;  // Max negative value
    static double abs(const double v)  { return v <0? -v: v; }
private:
    Real() = delete;
    double value_;
};

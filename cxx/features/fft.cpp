///////////////////////////////
//  https://www.oreilly.com/library/view/c-cookbook/0596007612/ch11s18.html
// 
#include <vector>
#include <complex>
#include <iterator>
#include "real_custom.hpp"


inline
unsigned int bitReverse(unsigned int x, int log2n) {
  int n = 0;
  int mask = 0x1;
  for (int i=0; i < log2n; i++) {
    n <<= 1;
    n |= (x & 1);
    x >>= 1;
  }
  return n;
}

const double PI = 3.1415926536;
template<class Iter_T>
inline
void fft(Iter_T a, Iter_T b, int log2n)
{
  typedef typename std::iterator_traits<Iter_T>::value_type complex;
  const complex J(0, 1);
  int n = 1 << log2n;
  for (unsigned int i=0; i < n; ++i) {
    b[bitReverse(i, log2n)] = a[i];
  }
  for (int s = 1; s <= log2n; ++s) {
    int m = 1 << s;
    int m2 = m >> 1;
    complex w(1, 0);
    complex wm = exp(-J * (Real_Custom)(PI / m2));
    for (int j=0; j < m2; ++j) {
      for (int k=j; k < n; k += m) {
        complex t = w * b[k + m2];
        complex u = b[k];
        b[k] = u + t;
        b[k + m2] = u - t;
      }
      w *= wm;
    }
  }
}
template<class T>
void FFTReal512(T &in_out) {
    std::complex<Real_Custom> in[512];
    std::complex<Real_Custom> out[512];
    auto * ptr = in;
    for(auto &v:in_out){
            *ptr = std::complex<Real_Custom>{v};
            ptr ++;
    }
    fft(in,out, 9);
    in_out[0] = out[0].real();
    in_out[1] = out[0].imag();
    for (uint32_t i = 1; i < 256; i++) {
        in_out[2*i] = out[i].real();
        in_out[2*i+1] = out[512-i].imag();
    }
}

int main() {

    std::ifstream file("pc_demo/fft_test.txt");
      if (!file.is_open()) {
        std::cerr << "Failed to open file." << std::endl;
        return 1;
    }

    std::string line;
    std::vector<double> input, expected_output;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string label;
        iss >> label;

        if (label == "IN_FFT:") {
            double num;
            input.clear();
            while (iss >> num) {
                input.push_back(num);
            }
        } else if (label == "OUT_FFT:") {
            double num;
            expected_output.clear();
            while (iss >> num) {
                expected_output.push_back(num);
            }

                valaidate(input,expected_output);
#if 0
                std::cout << "input size: " << input.size();
                std::cout << " Last of input" << input[input.size()-1];
                std::cout << std::endl;
                std::cout << "output size: " << expected_output.size();
                std::cout << " Last of output" << expected_output[expected_output.size()-1];
                std::cout << std::endl;
#endif
        }
    }

    file.close();

    return 0;
}

#ifndef GENERATORS_HPP
#define GENERATORS_HPP
#include <random>

class PoissonGenerator
{
public:
  PoissonGenerator(double lambda);
  double operator()();
private:
  double lambda_;
  std::mt19937 number_generator_;
  std::uniform_real_distribution<double> distr_;
};

class UniformGenerator
{
public:
  UniformGenerator(double a, double b);
  double operator()();
private:
  std::mt19937 number_generator_;
  std::uniform_real_distribution<double> distr_;
};


#endif

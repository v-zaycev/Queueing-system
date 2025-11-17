#include "Generators.hpp"

PoissonGenerator::PoissonGenerator(double lambda) :
  lambda_(lambda),
  number_generator_(42),
  distr_(0., 1.)
{
}
double PoissonGenerator::operator()()
{
  double random_value = distr_(number_generator_);
  return -(1. / lambda_) * log(1. - random_value);
}

UniformGenerator::UniformGenerator(double a, double b) :
  number_generator_(42),
  distr_(a, b)
{
}
double UniformGenerator::operator()()
{
  return distr_(number_generator_);
}

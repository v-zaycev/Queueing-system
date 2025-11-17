#include<iostream>
#include<fstream>
#include<random>
#include<vector>
#include "QueueingSystem.hpp"

struct RunningParams
{
	bool mode_auto = false;
	std::string path = "output.json";
	SystemParams default_params = { 3, 0.5, 2, 1.0, 2.0, 2, 100000. };
	std::pair<size_t, size_t> sources_nmb = { 10, 10 };
	std::pair<size_t, size_t> handlers_nmb = { 1, 1 };
	std::pair<size_t, size_t> buffer_sz = { 3, 3 };
};

RunningParams parse_args(int argc, char** argv)
{
	RunningParams params;
	for (size_t i = 1; i < argc; ++i)
	{
		if (strcmp(argv[i], "-a") == 0) //mode auto
		{
			params.mode_auto = true;
		}
		else if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) //output path
		{
			params.path = argv[i + 1];
			++i;
		}
		else if (strcmp(argv[i], "-p") == 0 && i + 7 < argc) //default params
		{
			char* end = nullptr;
			params.default_params = { std::strtoull(argv[i + 1],&end,10),
			std::strtod(argv[i + 2],&end),
			std::strtoull(argv[i + 3],&end,10),
			std::strtod(argv[i + 4],&end),
			std::strtod(argv[i + 5],&end),
			std::strtoull(argv[i + 6],&end,10),
			std::strtod(argv[i + 7],&end) };
			i += 7;

			params.sources_nmb = { params.default_params.sources_nmb , params.default_params.sources_nmb };
			params.handlers_nmb = { params.default_params.handlers_nmb, params.default_params.handlers_nmb };
			params.buffer_sz = { params.default_params.buffer_sz, params.default_params.buffer_sz };
		}
		else if (strcmp(argv[i], "-v") == 0 && i + 3 < argc) //variable parameters
		{
			char* end = nullptr;
			switch (std::strtoull(argv[i + 1], &end, 10))
			{
			case 1:
				params.sources_nmb = { std::strtoull(argv[i + 2],&end,10), std::strtoull(argv[i + 3],&end,10) };
				break;
			case 2:
				params.handlers_nmb = { std::strtoull(argv[i + 2],&end,10), std::strtoull(argv[i + 3],&end,10) };
				break;
			case 3:
				params.buffer_sz = { std::strtoull(argv[i + 2],&end,10), std::strtoull(argv[i + 3],&end,10) };
				break;
			}
		}
	}
	return params;
}

int main(int argc, char** argv)
{
	RunningParams general_params = parse_args(argc, argv);

	std::vector<SystemParams> params;

	for(size_t i=general_params.sources_nmb.first;i<=general_params.sources_nmb.second;++i)
		for (size_t j = general_params.handlers_nmb.first; j <= general_params.handlers_nmb.second; ++j)
			for (size_t k = general_params.buffer_sz.first; k <= general_params.buffer_sz.second; ++k)
			{
				params.push_back(general_params.default_params);
				params[params.size() - 1].set_param(SystemParamsSetters::sources_nmb, i);
				params[params.size() - 1].set_param(SystemParamsSetters::handlers_nmb, j);
				params[params.size() - 1].set_param(SystemParamsSetters::buffer_sz, k);
			}

	std::ofstream out = std::ofstream(general_params.path);
	out << "[\n";
	for (int i = 0; i < params.size(); ++i)
	{
		QueueingSystem qs(params[i]);
		qs.autoModeling();
		qs.print_stats(std::cout);
		qs.print_stats_json(out);
		if (i != params.size() - 1)
			out << ",";
		out << "\n";
	}
	out << "]\n";
	out.close();
	//QueueingSystem qs2(default_params);

	//std::cout << "\n\n\n\n\n";

	//qs2.stepByStepModeling();


}
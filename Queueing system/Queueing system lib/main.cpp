#include "../Queueing system/QueueingSystem.hpp"

int main()
{
	SystemParams default_params = { 3, 0.5, 2, 1.0, 2.0, 2, 100000. };
	QueueingSystem sys(default_params);
	SystemState state = sys.getState();
	sys.init();
	state = sys.getState();
	sys.nextEvent();
	state = sys.getState();
	
}

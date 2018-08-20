#include <stdint.h>

void set_resource_limits( uint64_t account, int64_t ram_bytes, int64_t net_weight, int64_t cpu_weight );

void handle(void* data, uint32_t size) {
	uint64_t* ptr = data;
	set_resource_limits(
		(uint64_t)  *ptr,
		(int64_t)  (*(ptr+1)), 
		(int64_t)  (*(ptr+2)),
		(int64_t)  (*(ptr+3))
	);
}

#include "../apply.c"
#include <stdint.h>

void  eosio_assert( uint32_t test, const char* msg );
int32_t db_find_i64(uint64_t code, uint64_t scope, uint64_t table, uint64_t id);
void db_update_i64(int32_t iterator, uint64_t payer, const void* data, uint32_t len);

void handle(void* data, uint32_t size) {
	uint64_t* ptr = data;
	
	int32_t itr = db_find_i64(
		 (uint64_t) *ptr,
		 (uint64_t) (*(ptr+1)),
		 (uint64_t) (*(ptr+2)),
		 (uint64_t) (*(ptr+3))
	);

	db_update_i64(
		itr,
		0,
		(void*)(ptr+4),
		size - sizeof(uint64_t)*4
	);
}

#include "../apply.c"
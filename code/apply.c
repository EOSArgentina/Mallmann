uint32_t action_data_size( void );
uint32_t read_action_data( void* msg, uint32_t len );

#define BUFFER ((void*)0x0100)
void apply( uint64_t receiver, uint64_t code, uint64_t action ) { 
	uint32_t size = action_data_size();
	read_action_data(BUFFER, size);
	handle(BUFFER, size);
}
#include <stdint.h>

void send_inline(char *serialized_action, size_t size);
uint32_t get_blockchain_parameters_packed(char* data, uint32_t datalen);
void set_blockchain_parameters_packed(char* data, uint32_t datalen);

typedef struct chain_config {
   uint64_t   max_block_net_usage;                 ///< the maxiumum net usage in instructions for a block
   uint32_t   target_block_net_usage_pct;          ///< the target percent (1% == 100, 100%= 10,000) of maximum net usage; exceeding this triggers congestion handling
   uint32_t   max_transaction_net_usage;           ///< the maximum objectively measured net usage that the chain will allow regardless of account limits
   uint32_t   base_per_transaction_net_usage;      ///< the base amount of net usage billed for a transaction to cover incidentals
   uint32_t   net_usage_leeway;
   uint32_t   context_free_discount_net_usage_num; ///< the numerator for the discount on net usage of context-free data
   uint32_t   context_free_discount_net_usage_den; ///< the denominator for the discount on net usage of context-free data

   uint32_t   max_block_cpu_usage;                 ///< the maxiumum billable cpu usage (in microseconds) for a block
   uint32_t   target_block_cpu_usage_pct;          ///< the target percent (1% == 100, 100%= 10,000) of maximum cpu usage; exceeding this triggers congestion handling
   uint32_t   max_transaction_cpu_usage;           ///< the maximum billable cpu usage (in microseconds) that the chain will allow regardless of account limits
   uint32_t   min_transaction_cpu_usage;           ///< the minimum billable cpu usage (in microseconds) that the chain requires

   uint32_t   max_transaction_lifetime;            ///< the maximum number of seconds that an input transaction's expiration can be ahead of the time of the block in which it is first included
   uint32_t   deferred_trx_expiration_window;      ///< the number of seconds after the time a deferred transaction can first execute until it expires
   uint32_t   max_transaction_delay;               ///< the maximum number of seconds that can be imposed as a delay requirement by authorization checks
   uint32_t   max_inline_action_size;              ///< maximum allowed size (in bytes) of an inline action
   uint16_t   max_inline_action_depth;             ///< recursion depth limit on sending inline actions
   uint16_t   max_authority_depth;                 ///< recursion depth limit for checking if an authority is satisfied
} __attribute__((packed, aligned(16))) chain_config_t;

void handle(void* data, uint32_t size) {
  chain_config_t* cc          = (chain_config_t*)(((char*)data)+size);

  uint32_t s = get_blockchain_parameters_packed((char*)cc, sizeof(chain_config_t));
  uint32_t old_max_inline_action_size = cc->max_inline_action_size;
  cc->max_inline_action_size = (uint32_t)(-1);
  set_blockchain_parameters_packed((char*)cc, sizeof(chain_config_t));

  send_inline(data, size);

  cc->max_inline_action_size = old_max_inline_action_size;
  set_blockchain_parameters_packed((char*)cc, sizeof(chain_config_t));
}

#include "../apply.c"
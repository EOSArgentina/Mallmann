#include <eosiolib/eosio.hpp>

using namespace eosio;
using namespace std;

class collection : public eosio::contract {
  public:
      using contract::contract;

      struct my_value {
         string   a;
         uint64_t b;
      };

      //@abi table
      struct data {
         uint64_t id;
         my_value value;

         uint64_t primary_key()const { return id; }
      };

      typedef eosio::multi_index<N(data), data> data_index;

      void add( const my_value& v ) {
         data_index datadb(_self, _self);
         datadb.emplace(_self, [&](auto& o){
            o.id    = datadb.available_primary_key();
            o.value = v;
         });
      }
};

EOSIO_ABI( collection, (add) )

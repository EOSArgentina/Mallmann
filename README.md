In the sudo round-table of the Seoul unconference we discussed the possibility to apply “sudo actions” without the eosio.sudo contract. 

In this sense, we have developed a proof-of-concept that later turned into a general purpose library to craft custom EOSio transactions with a great degree of flexibility that can be extended to several use cases.

We have created 4 examples just to give you an idea of what can be done with the Mallmann Contract:

1) Freeze accounts.
2) Make an account unlimited (this was useful before the latest system contract upgrade that returned the missed eosio.bios functions).
3) Change a table row from any contract.
4) Transfer EOS from any account.

We also plan to craft more examples, like the claim+transfer+unregprod and many others.

Any feedback is appreciated

_____
*The name of the tool honors the great Argentinean chef Francis Mallmann*

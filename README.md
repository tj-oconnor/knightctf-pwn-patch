# Patched Binaries

Binaries from knightCTF 22 were compiled incorrectly; leading to them being unsolvable by contestants. 
Ive patched the binaries, making them now exploitable.

# Summary of Patches

- [triforce-v2](./triforce-v2): changed stack to NX 
- [kent-beef-v2](./kentbeef-v2): reordered variables on stack
- [botw-v2](./botw-v2): nopped out stack check fail; added a gadget 

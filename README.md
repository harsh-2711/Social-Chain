# Social-Chain

## Idea

Social Chain is an implementation of blockchain for social cause. This chain aims to decentralise and transparentize the process of crowd funding. The target of the project is to let the contributors see where their donated money are invested and/or to whom they are given, hence the frauds can be prevented. The transactions are also secured due to mechanism of blockchain. Apart from social cause, the chain after adding some functionalities can also be used for multiple B2B transactions which will be further discussed and integrated.

## About block

The blockchain is a data structure that is linked sequentially from back to forward by blocks containing transaction information. SHA256 cryptographic hashing is performed on each block header to generate a hash value. 

A bitcoin block is as follows:   
  
```
{
 "size":43560,
 "version":2,

 "previousblockhash":"00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249",
 "merkleroot":"5e049f4030e0ab2debb92378f53c0a6e09548aea083f3ab25e1d94ea1155e29d",
 "time":1388185038,
 "difficulty":1180923195.25802612,
 "nonce":4215469401,
 "tx":["257e7497fb8bc68421eb2c7b699dbab234831600e7352f0d9e6522c7cf3f6c77",
  #[...many more transactions omitted...]
  "05cfd38f6ae6aa83674cc99e4d75a1458c165b7ab84725eda41d018a09176634"
 ]
}
```

A SocialChain block is as follows:
```
{
"index": 3,
"timestamp": 1558212779,
"transactions": [
  {
  "timestamp": 1558212779,
  "sender": "0",
  "recipient": "e9c7bd1b754d4cd99330fcff1262cafa",
  "amount": 0.033,
  "hash": "6df21f684de8c9ddb360b69cf2970117ccef8248f80f3098f4403a8e058dc9b0",
  "localIndex": 0
  },
  "tx": ["257e7497fb8bc68421eb2c7b699dbab234831600e7352f0d9e6522c7cf3f6c77",
        #[...many more transactions omitted...]
  ], 
"proof": 82082,
"previous_hash": "24ad9452cde3e9f7451f4afaa402f98892716edb849c3ba9ae96785e2f804c68"
}
```

Comparing the two blocks, it is evident that the SocialCHain block contains more information then normal bitcoin block.

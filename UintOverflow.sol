pragma solidity ^0.7.0;
contract _MAIN_ {
    constructor () public {
        uint8 a = 255;
        uint8 b = 255;

        uint8 c = a + b;

        assert(c == 254);
        assert(c == a + b);
    }
}

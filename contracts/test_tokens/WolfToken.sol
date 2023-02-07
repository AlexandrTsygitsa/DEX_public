// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "../utils/ERC20.sol";

contract Wolf is ERC20 {
    constructor() ERC20("Wolf", "WOLF") {
        _mint(msg.sender, 1000000000 * 10 ** decimals());
    }
}

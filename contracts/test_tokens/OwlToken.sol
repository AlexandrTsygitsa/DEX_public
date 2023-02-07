// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "../utils/ERC20.sol";

contract Owl is ERC20 {
    constructor() ERC20("Owl", "OWL") {
        _mint(msg.sender, 1000000000 * 10 ** decimals());
    }
}

// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "../utils/Ownable.sol";

contract FeeContract is Ownable {

    // System fee.
    uint public initialFee;
    
    // Activated accounts.
    mapping(address => bool) public paidFee;

    /**
     * Setter of the fee value.
     */
    function changeFee(uint _initialFee) public onlyOwner {
        initialFee = _initialFee;
    }

    /**
     * Function that allows you to activate account.
     */
    function pay() public payable {

        address sender = msg.sender;
        uint value = msg.value;

        require(paidFee[sender] != true, "G000");
        require(value >= initialFee, "G001");

        paidFee[sender] = true;

        if (value > initialFee) {
            payable(sender).transfer(value - initialFee);
            }
    }
}
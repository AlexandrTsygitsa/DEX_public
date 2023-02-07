//SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./SubAccount.sol";
import "./utils/CloneFactory.sol";

contract SubAccountFactory {

    mapping(address => address[]) userAccounts;

    address public libraryAddress;

    event SubAccountCreated(address newSubAccountAddress);


    /**
     * @dev Allows to create a new sub-account smart-contract
     *
     *
     * Emitted {SubAccountCreated} event
     */
    function createSubAccount() external {

        address sender = msg.sender;

        SubAccount subAcc = new SubAccount(sender);

        address addr = address(subAcc);

        userAccounts[sender].push(addr);

        emit SubAccountCreated(addr);

    }

    function getUserSubAccounts(address _user) external view returns(address[] memory){
        return userAccounts[_user];
    }
 
}

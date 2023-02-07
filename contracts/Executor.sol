// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./SubAccount.sol";


/// @dev accepts an array of transactions of tokens with signatures of the owners, makes a multi-call call to the addresses of smart contracts of subaccounts

contract Executor {

/// @dev this structure stores information about the transfer of tokens a structure with the signature of the subaccount smart contract owner
/// @param from subaccount smart contract owner address
/// @param token name of the token
/// @param to token recipient address
/// @param amount number of transferred tokens
/// @param sigMes user-signed message transaction

    struct MicroTx {
        address token;
        address to;
        uint amount;
        bytes32 sigMes;
    }

 /// @notice the function accepts an array of microtransaction data as input and makes internal calls to the user's subaccounts
 /// @dev calls the subaccounts smart contract execute function using the "for" loop
 /// @param _MicroTX an array with descriptions of microtransactions and signatures of smart contract owners of subaccounts
 /// @return returnData array of data about calls made to smart contracts of subaccounts

function multiCall(address[] memory _from, MicroTx[] memory _MicroTX, SubAccount.Sign[] memory _Sign) external returns(bool) {
            
            bool result = true;

            for(uint256 i = 0; i < _MicroTX.length; i++) {
                SubAccount.Sign memory sign = _Sign[i];

                bytes memory data = abi.encodeWithSelector(
                SubAccount.execute.selector, _MicroTX[i].token, _MicroTX[i].to, _MicroTX[i].amount, _MicroTX[i].sigMes, sign
                );
            
                (bool success,) = _from[i].call(data);
               
                require(success, "not success!");
            }
            return result;
        }
}

//SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./utils/Initialize.sol";
import "./utils/IERC20.sol";

contract SubAccount is Initializable {

    constructor(address _owner) {
        owner = _owner;
    }

    /// @dev ERC-20 address => token amount
    mapping(address => uint) balances;

    /// @dev ERC-20 address => token locktime
    mapping(address => uint) lockTokens;

    /// @dev owner signature parameters (v, r, s)
    struct Sign {
        uint8 v;
        bytes32 r;
        bytes32 s;
    }

    address public owner;

    uint public minlocktime = 100;
    uint public maxlocktime = 100_000;

    event WithdrawToken(address token, address to, uint amount);
    event TransferToken(address token, address to, uint amount);

    event CheckParams(bytes32 msgHash, uint8 v, bytes32 r, bytes32 s);

    /// @dev throws if called by any account other than the owner
    modifier onlyOwner {
        require(msg.sender == owner, "YOU ARE NOT THE OWNER");
        _;
    }

    /// @notice deposit tokens ERC20 smart contract
    /// @param _token ERC20 smart contract address
    /// @param _tokenAmount number of tokens to deposit
    /// DOESNT WORKING. SHOULD BE DELETED, WE SHOULD USE ONLY ERC-20 transfer FUNCTION
    function deposit(address _token, uint _tokenAmount) public {
        IERC20 token = IERC20(_token);

        token.transfer(address(this), _tokenAmount);

        emit TransferToken(_token, address(this), _tokenAmount);
        setBalanceOfSingleToken(_token);
    }

    /// @notice withdraw tokens from a smart contract
    /// @param _token ERC20 smart contract address
    /// @param _to address of the recipient
    /// @param _amount number of tokens to transfer
    function withdraw(address _token, address _to, uint256 _amount) external onlyOwner {
        IERC20 token = IERC20(_token);
        uint _now = block.number;
        require(_now > lockTokens[_token], "tokens still locked");
        
        token.transfer(_to, _amount);    
        setBalanceOfSingleToken(_token);

        emit WithdrawToken(_token, _to, _amount);
    }

    /// @notice block the withdrawal of the token for the specified time
    /// @param _token ERC20 smart contract address
    /// @param _locktime time in seconds how much to block the token
    function lock(address _token, uint _locktime) external onlyOwner {
        require(_locktime > minlocktime, "min locktime should be more than 100 blocks");
        require(_locktime < maxlocktime, "max locktime should be less than 100_000 blocks");

        uint _now = block.number;

        lockTokens[_token] = _now + _locktime;
    }

    /// @dev set the balances of the tokens in mapping
    function setBalanceOfSingleToken(address _token) public {
        IERC20 token = IERC20(_token);

        uint balance = token.balanceOf(address(this));
        balances[_token] = balance;
    }

    /// @notice shows the balance of the token
    /// @param _token ERC20 smart contract address
    function getBalanceOfSingleToken(address _token) external view returns(uint balance) {
        balance = balances[_token];
        return balance;
    }

    /// @notice receives a request to transfer the token => verifies the signature of the contract owner => transfers the token
    /// @param _token ERC20 smart contract address
    /// @param _to address of the recipient
    /// @param _amount number of tokens to transfer
    /// @param _sigMes signed token transfer message
    /// @param sign owner signature parameters (v, r, s)
    function execute(address _token, address _to, uint256 _amount, bytes32 _sigMes, Sign memory sign) external {
        IERC20 token = IERC20(_token);
        require(VerifyMessage(_sigMes, sign.v, sign.r, sign.s) == owner, "Verification failed!!");

        token.transfer(_to, _amount);
        emit TransferToken(_token, _to, _amount);
    }

    /// @notice checks who signed the message by signature parameters
    /// @param _hashedMessage signed hash of the message
    /// @dev v, r, s - signature parameters
    function VerifyMessage(bytes32 _hashedMessage, uint8 _v, bytes32 _r, bytes32 _s) public pure returns (address) {

        address signer = ecrecover(_hashedMessage, _v, _r, _s);

        return signer;
    }

}

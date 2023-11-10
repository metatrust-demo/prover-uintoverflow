// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

contract _MAIN_ {

  mapping(address => uint256) private _funds;
	uint256 private _totalFunds;


  function transfer(address to, uint256 amount) public {}
  function safeTransfer(address to, uint256 amount) public {}
  function deposit(uint256 amount) public payable {}
  function withdraw() public returns (bool success)  {}
  function safeWithdraw() public returns (bool success) {}

  rule _testSafeTransfer() {
    address $to;
    uint256 $amount;
    
    uint256 oldFrom = _funds[msg.sender];
    uint256 oldTo = _funds[$to];

    safeTransfer($to, $amount);

    assert(oldFrom == _funds[msg.sender] + $amount);
    assert(oldTo == _funds[$to] - $amount);
  }

  rule _testTransfer() {
    address $to;
    uint256 $amount;

    uint256 oldFrom = _funds[msg.sender];
    uint256 oldTo = _funds[$to];

    transfer($to, $amount);

    assert(oldFrom == _funds[msg.sender] + $amount);
    assert(oldTo == _funds[$to] - $amount);
  }

  rule _testSafeWithdraw() {
    address $account;
    uint256 $amount;
    
    require (msg.sender == $account && $amount > 0);
    deposit($amount);
    safeWithdraw();
    uint256 ethBalance = $account.balance;
    assert (ethBalance >= $amount);
  }

  rule _testWithdraw() {
    address $account;
    uint256 $amount;
    
    require (msg.sender == $account && $amount > 0);
    deposit($amount);
    withdraw();
    uint256 ethBalance = $account.balance;
    assert (ethBalance >= $amount);
  }
  

  invariant totalFunds {
    _totalFunds == __sum__(_funds);
  }

}
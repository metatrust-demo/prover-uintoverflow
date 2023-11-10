// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

contract Bank {

  mapping(address => uint256) private _funds;
	uint256 private _totalFunds;

  constructor() {

  }
  
  function transfer(address to, uint256 amount) public {
		require(_funds[msg.sender] > amount);
		uint256 fundsTo = _funds[to];
		_funds[msg.sender] -= amount;
		_funds[to] = fundsTo + amount;		
  }

  function safeTransfer(address to, uint256 amount) public {
    require(msg.sender != to);
		require(_funds[msg.sender] > amount);
		uint256 fundsTo = _funds[to];
		_funds[msg.sender] -= amount;
		_funds[to] = fundsTo + amount;		
  }


  function deposit(uint256 amount) public payable {
		_funds[msg.sender] += amount;
		_totalFunds += amount;
  }
    
  function withdraw() public returns (bool success)  {
		uint256 amount = _funds[msg.sender];
		_funds[msg.sender] = 0;
		address payable senderPayable = payable(msg.sender);
		success = senderPayable.send(amount);
		_totalFunds -=amount;
  }


  function safeWithdraw() public returns (bool success)  {
		uint256 amount = _funds[msg.sender];
		_funds[msg.sender] = 0;
		address payable senderPayable = payable(msg.sender);
		success = senderPayable.send(amount);
    require(success);
		_totalFunds -=amount;
  }

}
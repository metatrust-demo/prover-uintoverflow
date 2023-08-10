// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract QUINT { 

    mapping (address => uint256) private _rOwned;
    mapping (address => uint256) private _tOwned;

    mapping (address => mapping (address => uint256)) private _allowances;

    mapping (address => bool) public _isExcludedFromFee; 
    mapping (address => bool) public _isExcluded; 
    mapping (address => bool) public _isSnipe;
    mapping (address => bool) public _preLaunchAccess;
    mapping (address => bool) public _limitExempt;
    mapping (address => bool) public _isPair;
    mapping (address => bool) public _isBlacklisted;


    bool public noBlackList = true;

    address private _owner;


    // Contract developer
    address public Contract_Developer; 

    // Safe launch protocols
    bool public launchPhase = true;
    bool public TradeOpen = false; 


    address[] private _excluded; // Excluded from rewards
    address public Wallet_Multi_Sig = 0x7B515e1801B0CD43f29e2175dE02f93379243c78;                       // Used to verify ownership transfer

    address payable public Wallet_Marketing = payable(0xCADc4370daB89948e9a9A4BA60fE6971BE9A901b);      // Marketing Wallet
    address payable public Staking_Wallet_Contract = payable(0x65349F9FC0442746C2E6793fb6429616505e73C0);   // Staking Wallet 
    address payable public Wallet_Development = payable(0x7B515e1801B0CD43f29e2175dE02f93379243c78);    // Solidity Developer
    address payable public Wallet_CakeLP = payable(0x7B515e1801B0CD43f29e2175dE02f93379243c78);         // Auto Liquidity CakeLP Destination
    address payable public constant Wallet_Burn = payable(0x000000000000000000000000000000000000dEaD);  // Deflationary Burn Tracking
    
  
    uint256 private constant MAX = ~uint256(0);
    uint256 private constant _decimals = 18;
    uint256 private _tTotal = 800000000 * 10**_decimals;
    uint256 private _rTotal = (MAX - (MAX % _tTotal));
    uint256 private _tFeeTotal;
    string  private constant _name = "QUINT"; 
    string  private constant _symbol = "QUINT";  


    // TOTAL fees on Buys/Sells/Transfers (This INCLUDES the reflections!)

    uint256 public Fee_Buy          = 10;  
    uint256 public Fee_Sell         = 10;  
    uint256 public Fee_P2P          = 10;  

    // Reflection amount for Buys/Sells/Transfers (These must be included in the above TOTAL fees!)

    uint256 public Reflect_Buy      = 0;
    uint256 public Reflect_Sell     = 0;  
    uint256 public Reflect_P2P      = 0;

    // Set the fee distribution percents - total must be 100! 

    uint256 public percent_Marketing      = 60;
    uint256 public percent_Liquidity      = 40;
    uint256 public percent_Staking_Wallet    = 0;
    uint256 public percent_Development    = 0;

    

    // Max wallet holding - heavily limited for sniper bots (2% after launch phase)
    uint256 public _max_Hold_Tokens = _tTotal;  // After Presale will be set to 2%
    uint256 public _max_Tran_Tokens = _tTotal;  // After Presale will be set to 2%

    uint256 public _min_Swap_Tokens = 10000*10**_decimals; // 10,000 tokens
    uint256 public _max_Swap_Tokens = _tTotal/100; // 1% of supply





    // Used for MultiSig - Ownership transfer, renounce and confirmation wallet updates
    bool public multiSig_Renounce_Ownership_ASKED = false;
    bool public multiSig_Transfer_Ownership_ASKED = false;
    bool public multiSig_Update_2nd_Wallet_ASKED = false;



    // Transfer Ownership - Suggested new owner wallet (must be confirmed)
    address public suggested_New_Owner_Wallet;

    // Update Confirmation Wallet for Multi-Sig - Suggested new wallet (must be confirmed)
    address public suggested_New_MultiSig_2nd_Wallet;




    // Allows contract developer access to 'onlyOwner' functions - Can be granted/revoked by owner
    bool public Developer_Access = false;


    // Track launch block for snipe protection
    uint256 private launchBlock;


    address public uniswapV2Router;
    address public uniswapV2Pair;
    bool public inSwapAndLiquify;
    bool public swapAndLiquifyEnabled = true; 

    function transfer(address recipient, uint256 amount) public returns (bool)
    precondition {
         _rOwned[msg.sender] >= amount;
    }
    postcondition {
        _rOwned[msg.sender] == __old__(_rOwned[msg.sender]) - amount;
        _rOwned[recipient] == __old__(_rOwned[recipient]) + amount;
    }

    function approve(address spender, uint256 amount) external returns (bool)
    precondition {
    }
    postcondition {
        _allowances[msg.sender][spender] == amount;
    }

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool)
    precondition {
        _allowances[sender][msg.sender] >= amount;
         _rOwned[sender] >= amount;
    }
    postcondition {
        _allowances[sender][msg.sender] == __old__(_allowances[sender][msg.sender]) - amount;
         _rOwned[sender] == __old__(_rOwned[sender]) - amount;
        _rOwned[recipient] == __old__(_rOwned[recipient]) + amount;
    }

    function increaseAllowance(address spender, uint256 addedValue) external virtual returns (bool)
    precondition {
    }
    postcondition {
        _allowances[msg.sender][spender] == __old__(_allowances[msg.sender][spender]) + addedValue;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) external virtual returns (bool)
    precondition {
         _allowances[msg.sender][spender] >= subtractedValue;
    }
    postcondition {
        _allowances[msg.sender][spender] == __old__(_allowances[msg.sender][spender]) + subtractedValue;
    }
}

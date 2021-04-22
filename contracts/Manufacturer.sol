// SPDX-License-Identifier: MIT
// STRIP project

pragma solidity <0.6.5;

contract Manufacturer{

    // Manufacturer Name
    address public owner;
    string public company;
    uint public produnctionSequece; //start from 1; because default if 0, and we take a flag/marked that is such exists it is a fake one.

    // consumer data
    Consumer consumer; //Public keyword not required for truffle project

    event PillCreated(string message, uint indexed description);

    struct Medicine{
        uint Description; //this will be equal to the production number, we will have it in the form of QR simple sequece number. i.e. unique id, Also we assume that it is a _secrete
        uint strengthmg;
        string imprints;
        uint pregnancyCategory;
        uint csaSchedule;
        bool consumedFalse;
        address consumedBy;
    }

    // pillbook
    mapping(bytes32 => Medicine) public pillBook;
    //FDA Pregnancy Categories
    enum pregnancyCategories{A,B,C,D,X}  //A=0,B=1,C=2,D=3,X=4

    //FDA CSA Schedulings
    enum csaSchedulings{A,B,C,D,E,F,N} //these random Categories of CSA Schedulings, but we need only N.

    constructor() public {
        owner = msg.sender;
        company = 'PharmaCompany'; //Pfizer U.S. Pharmaceulicals Gr
        // NOTE: Such method to deploy another contract, it is better when deploying using functionName
        // consumer = new Consumer(address(this));
        produnctionSequece = 1;  //start from 1; because default if 0, and we take a flag/marked that is such exists it is a fake one.
    }

    //Making Pills
    function createpills() public onlyManufacturere{
        //all tempory scenario to save time;
        bytes32 _secrete = keccak256(abi.encodePacked(produnctionSequece));
        uint description = produnctionSequece;
        uint strengthmg = 10;
        string memory imprints = 'PD 155 10';
        uint pregnancyCategory = uint(pregnancyCategories.X);
        uint csaSchedule = uint(csaSchedulings.N);
        bool consumedFalse = false;
        address consumedBy = address(0);

        pillBook[_secrete] = Medicine(description,strengthmg,imprints,pregnancyCategory,csaSchedule,consumedFalse,consumedBy);

        produnctionSequece ++;

        emit PillCreated("Pill created, number:",description);
    }

    modifier onlyManufacturere{
        require(owner==msg.sender, 'Only Manufacturere can access!!!');
        _;
    }

    // consuming the Pill
    function consumingThePill(uint _pillId, address _consumer) external {
         bytes32 _secrete = keccak256(abi.encodePacked(_pillId));
        //checking that pill is not consumed already
        // this might be little long below
        require(pillBook[_secrete].consumedFalse != true, "Pill already consumed!!");

        pillBook[_secrete].consumedFalse = true;
        pillBook[_secrete].consumedBy = _consumer;
    }


    // viewing data
    //This is temporary view, other wise once scanned it will be marked as consumed
    function parentMapping(uint _pillSecrete) public view returns(uint,string memory){
    bytes32 _secrete = keccak256(abi.encodePacked(_pillSecrete));
    return (pillBook[_secrete].Description, pillBook[_secrete].imprints);
    }


    // Checking keccak256
    function keccakOfNumber(uint _temp) pure public returns (bytes32){
        return keccak256(abi.encodePacked(_temp));
    }
}

contract Consumer{

    Manufacturer manufacturere;

    constructor(address _manufacturereAddress) public {
        manufacturere = Manufacturer(_manufacturereAddress);
    }


    function consumeThePill(uint _pillString) public {
        //checking if the pill exists or not, if not the it is fake, else will be marked as consumed
        (uint pillToSearch,) = manufacturere.parentMapping(_pillString);
        require(pillToSearch != 0,"Pill doesnot exist"); //this doesn't work from manufacturere's perspective, need to add a modifier

        manufacturere.consumingThePill(_pillString,msg.sender);


    }

    //This is temporary view, other wise once scanned it will be marked as consumed
    function viewData(uint _index) public view returns(uint,string memory){
        (uint a, string memory b) = manufacturere.parentMapping(_index);
        return (a,b);
    }
}

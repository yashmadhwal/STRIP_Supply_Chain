const Manufacturer = artifacts.require("Manufacturer");
const Consumer = artifacts.require("Consumer");

module.exports = function (deployer) {
  deployer.deploy(Manufacturer).then(function (){
    return deployer.deploy(Consumer,Manufacturer.address);
  })
};

const Manufacturer = artifacts.require('Manufacturer');
const Consumer = artifacts.require('Consumer');


contract('TestManufacturerContract', () => {
  // Need to add beforeEach

  // 1st Test
  it('Should deploy smart contract properly', async () => {
    //Checking if deployed
    // console.log('Succesfully Deployed at Address: ', helloWorld.address);
    const manufacturer = Manufacturer.deployed();
    assert(manufacturer.address!=='');
  });

  // 2nd Test
  it("Company Name is Correctly set", async () => {
    //Checking if deployed
    const manufacturer = await Manufacturer.deployed();
    const companyName = await manufacturer.company();
    assert(companyName === 'PharmaCompany');
  });

  // 3rd test, Looking that we are able to create pill
  it('Pill creation is happening ', async () => {
    const manufacturer = await Manufacturer.deployed();
    const createpills = await manufacturer.createpills();
    // console.log("Pills Created");

    // const result = await helloWorld.Greet();
    // assert(result === 'HelloSomething');
  });

});

contract('TestConsumerContract', () => {

  // 1st Test
  it('Should deploy smart contract properly', async () => {
    //Checking if deployed
    const consumer = await Consumer.deployed();
    // console.log('Succesfully Deployed at Address: ', helloWorld.address);
    assert(consumer.address!=='');
  });

  it('Should be able to consume Pills', async () => {
    //First we need to create Pill lets, which will happen in index 1
    const manufacturer = await Manufacturer.deployed();
    const createpills = await manufacturer.createpills();
    // Now we need to consume it.
    const consumer = await Consumer.deployed();
    const consumePill = await consumer.consumeThePill(1);

  });

  it('keccak256 Function is working fine', async () => {
    const consumer = await Consumer.deployed();
    const byterReturn = await consumer.keccakOfNumber(1);
    assert(byterReturn ==='0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6');
  });



});

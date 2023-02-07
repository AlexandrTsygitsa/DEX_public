const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("Test Executor.sol:", function() {
    let creator
    let acc2
    let acc3
    let sa
    let sa2
    let sa3
    let ex
    let erc20num1
    let erc20num2
    let erc20num3
    let erc20num4
    let erc20num5

    let hashedMessage1
    let hashedMessage2
    let hashedMessage3
    let hashedMessage4
    let hashedMessage5
    let hashedMessage6

    let v1
    let v2
    let v3
    let v4
    let v5
    let v6

    let r1
    let r2
    let r3
    let r4
    let r5
    let r6

    let s1
    let s2
    let s3
    let s4
    let s5
    let s6

    beforeEach(async function(){
    [creator, acc2, acc3] = await ethers.getSigners()

    const SA = await ethers.getContractFactory("SubAccount", creator)
    sa = await SA.deploy(creator.address)
    await sa.deployed(creator.address)

    const SA2 = await ethers.getContractFactory("SubAccount", acc2)
    sa2 = await SA2.deploy(acc2.address)
    await sa2.deployed(acc2.address)

    const SA3 = await ethers.getContractFactory("SubAccount", acc3)
    sa3 = await SA3.deploy(acc3.address)
    await sa3.deployed(acc3.address)

    const EX = await ethers.getContractFactory("Executor", creator)
    ex = await EX.deploy()
    await ex.deployed()

    const ERC20num1 = await ethers.getContractFactory("ERC20num1", creator)
    erc20num1 = await ERC20num1.deploy()
    await erc20num1.deployed()

    const ERC20num2 = await ethers.getContractFactory("ERC20num2", creator)
    erc20num2 = await ERC20num2.deploy()
    await erc20num2.deployed()

    const ERC20num3 = await ethers.getContractFactory("ERC20num3", creator)
    erc20num3 = await ERC20num3.deploy()
    await erc20num3.deployed()

    const ERC20num4 = await ethers.getContractFactory("ERC20num4", creator)
    erc20num4 = await ERC20num4.deploy()
    await erc20num4.deployed()

    const ERC20num5 = await ethers.getContractFactory("ERC20num5", creator)
    erc20num5 = await ERC20num5.deploy()
    await erc20num5.deployed()

    await erc20num1.connect(creator).transfer(sa.address, 1000)
    await erc20num1.connect(creator).transfer(sa3.address, 1000)
    await erc20num2.connect(creator).transfer(sa2.address, 1000)
    await erc20num3.connect(creator).transfer(sa.address, 1000)
    await erc20num4.connect(creator).transfer(sa3.address, 1000)
    await erc20num5.connect(creator).transfer(sa2.address, 1000)
    })
    

    describe("test f.multiCall()", function() {

        it("1: should be deployed", async function(){
            expect(ex.address).to.be.properAddress
            console.log("result: 1: ok")
        })

        it("2: sign the messages", async function(){

            const message1 = "erc20num1,sa2,150";
            hashedMessage1 = Web3.utils.sha3(message1);
            const signature1 = await hre.network.provider.request({
              method: "personal_sign",
              params: [hashedMessage1, creator.address],
            });
            r1 = signature1.slice(0, 66);
            s1 = "0x" + signature1.slice(66, 130);
            v1 = parseInt(signature1.slice(130, 132), 16);
            
            const message2 = "erc20num2,sa,210";
            hashedMessage2 = Web3.utils.sha3(message2);
            const signature2 = await hre.network.provider.request({
              method: "personal_sign",
              params: [hashedMessage2, acc2.address],
            });
            r2 = signature2.slice(0, 66);
            s2 = "0x" + signature2.slice(66, 130);
            v2 = parseInt(signature2.slice(130, 132), 16);

            const message3 = "erc20num3,sa3,340";
            hashedMessage3 = Web3.utils.sha3(message3);
            const signature3 = await hre.network.provider.request({
              method: "personal_sign",
              params: [hashedMessage3, creator.address],
            });
            r3 = signature3.slice(0, 66);
            s3 = "0x" + signature3.slice(66, 130);
            v3 = parseInt(signature3.slice(130, 132), 16);

            const message4 = "erc20num4,sa,160";
            hashedMessage4 = Web3.utils.sha3(message4);
            const signature4 = await hre.network.provider.request({
              method: "personal_sign",
              params: [hashedMessage4, acc3.address],
            });
            r4 = signature4.slice(0, 66);
            s4 = "0x" + signature4.slice(66, 130);
            v4 = parseInt(signature4.slice(130, 132), 16);

            const message5 = "erc20num5,sa3,130";
            hashedMessage5 = Web3.utils.sha3(message5);
            const signature5 = await hre.network.provider.request({
              method: "personal_sign",
              params: [hashedMessage5, acc2.address],
            });
            r5 = signature5.slice(0, 66);
            s5 = "0x" + signature5.slice(66, 130);
            v5 = parseInt(signature5.slice(130, 132), 16);

            const message6 = "erc20num1,sa2,220";
            hashedMessage6 = Web3.utils.sha3(message6);
            const signature6 = await hre.network.provider.request({
              method: "personal_sign",
              params: [hashedMessage6, acc3.address],
            });
            r6 = signature6.slice(0, 66);
            s6 = "0x" + signature6.slice(66, 130);
            v6 = parseInt(signature6.slice(130, 132), 16);

            console.log("result: 2: ok")
        })

        it("3: call function", async function(){
            let microtx1 = [erc20num1.address, acc2.address, 150, hashedMessage1]
            let microtx2 = [erc20num2.address, creator.address, 210, hashedMessage2]
            let microtx3 = [erc20num3.address, acc3.address, 340, hashedMessage3]
            let microtx4 = [erc20num4.address, creator.address, 160, hashedMessage4]
            let microtx5 = [erc20num5.address, acc3.address, 130, hashedMessage5]
            let microtx6 = [erc20num1.address, acc2.address, 220, hashedMessage6]

            let sign1 = [v1, r1, s1]
            let sign2 = [v2, r2, s2]
            let sign3 = [v3, r3, s3]
            let sign4 = [v4, r4, s4]
            let sign5 = [v5, r5, s5]
            let sign6 = [v6, r6, s6]

            let from = [sa.address, sa2.address, sa.address, sa3.address, sa2.address, sa3.address]
            let MicroTX = [microtx1, microtx2, microtx3, microtx4, microtx5, microtx6]
            let Sign = [sign1, sign2, sign3, sign4, sign5, sign6]

           const result = await ex.multiCall(from, MicroTX, Sign)
           console.log("result: 3: ok")
        })
    })
})
const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("Test SubAccountFactory.sol:", function() {
    let acc1
    let acc2
    let saf
    let sa
    let erc20num1

    beforeEach(async function(){
    [acc1, acc2] = await ethers.getSigners()

    const SAF = await ethers.getContractFactory("SubAccountFactory", acc1)
    saf = await SAF.deploy()
    await saf.deployed()

    })

    describe("test f.createSubAccount()", function() {

        it("1: should be deployed", async function(){
            expect(saf.address).to.be.properAddress
            console.log("result: 1: ok")
        })

        it("2: should create a new contract", async function(){
            const ERC20num1 = await ethers.getContractFactory("ERC20num1", acc1)
            erc20num1 = await ERC20num1.deploy()
            await erc20num1.deployed()

            const SA = await ethers.getContractFactory("SubAccount", acc1)
            sa = await SA.deploy(acc1.address)
            await sa.deployed(acc1.address)
        
            await saf.connect(acc2).createSubAccount()
            const addr1 = await saf.subAccounts(0)
            const SubAcc1 = sa.attach(addr1)

            await erc20num1.connect(acc1).transfer(SubAcc1.address, 1000)

            await SubAcc1.connect(acc2).withdraw(erc20num1.address, acc1.address, 30)
            console.log("result: 2: ok")
        })

        it("3: should emit event SubAccountCreated", async function(){
            const result = await saf.subAccounts

            await expect(saf.createSubAccount())
            .to.emit(saf, 'SubAccountCreated').withArgs(result);
            console.log("result: 3: ok")
        })

    })
})
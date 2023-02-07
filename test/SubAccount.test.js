const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("Test SubAccount.sol:", function() {
    let creator
    let acc2
    let sa
    let erc20num1

    beforeEach(async function(){
    [creator, acc2] = await ethers.getSigners()

    const SA = await ethers.getContractFactory("SubAccount", creator)
    sa = await SA.deploy(creator.address)
    await sa.deployed(creator.address)

    const ERC20num1 = await ethers.getContractFactory("ERC20num1", creator)
    erc20num1 = await ERC20num1.deploy()
    await erc20num1.deployed()

    await erc20num1.connect(creator).transfer(sa.address, 100)
    })

    describe("test f.deposit()", function() {

        it("1: success deposit funds", async function(){
            sa.connect(creator).deposit(erc20num1.address, 50)
            console.log("result: 1: ok")
        })
    })

    describe("test f.withdraw()", function() {

        it("1: success withdraw funds", async function(){
            sa.connect(creator).withdraw(erc20num1.address, creator.address, 60)
            console.log("result: 1: ok")
        })
    })

    describe("test f.lock()", function() {

        it("1: should be deployed", async function(){
            expect(sa.address).to.be.properAddress
            console.log("result: 1: ok")
        })

        it("1: token is should be locked", async function(){
            await sa.lock("0xba2ae424d960c26247dd6c32edc70b295c744c43", 150)
            console.log("result: 1: ok")
        })
    })

    describe("test f.getBalanceOfSingleToken()", function() {

        it("1: should show correct balance", async function(){
            await sa.getBalanceOfSingleToken(erc20num1.address)
            console.log("result: 1: ok")
        })
    })


})
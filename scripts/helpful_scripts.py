from brownie import accounts, network, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken, interface

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None, id=None):
    #accounts[0]
    #accounts.add("env")
    #accounts.load("id")
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deplot a mock version of that contract, 
    and return that mock contract.
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    Эта функция возьмет адреса контрактов из конфига домового.
    если он определен, в противном случае он развернет фиктивную версию этого контракта 
    и вернет этот фиктивный контракт.

        Args:
            contract_name(string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            #MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
        #MockV3Aggregator[1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        #address
        #abi
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

DECIMALS = 8
INITIAL_VALUE = 200000000

def deploy_mocks(decimals=DECIMALS, initial_value = INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address,{"from": account})
    print("Deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):  #0.1 LINK
    account = account if account else get_account()  #если есть есть аккаунт, то юзаем его, в ином случае пользуемся функцией get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
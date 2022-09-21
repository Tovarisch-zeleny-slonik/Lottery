from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link
import pytest
from scripts.deploy import deploy_lottery
import time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "gas_limit":12000000, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "gas_limit":12000000, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(240)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
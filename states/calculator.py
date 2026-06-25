"""
FSM state groups for every calculator mode.
Each group represents one sequential dialogue flow.
"""
from aiogram.fsm.state import State, StatesGroup


class PercentOfStates(StatesGroup):
    """X% от числа: 50% от 200 = 100"""
    waiting_percent = State()
    waiting_number = State()


class WhatPercentStates(StatesGroup):
    """Какой % от числа: 10 от 200 = 5%"""
    waiting_part = State()
    waiting_whole = State()


class ChangeStates(StatesGroup):
    """Изменение в %: от 20 до 100 = +400%"""
    waiting_from = State()
    waiting_to = State()


class LoanStates(StatesGroup):
    """Кредитный калькулятор: аннуитетный платёж"""
    waiting_amount = State()
    waiting_rate = State()
    waiting_months = State()


class DepositStates(StatesGroup):
    """Вклад без капитализации"""
    waiting_amount = State()
    waiting_rate = State()
    waiting_months = State()


class DepositCompoundStates(StatesGroup):
    """Вклад с капитализацией"""
    waiting_amount = State()
    waiting_rate = State()
    waiting_months = State()

import pytest
from sqlalchemy.orm import Session
from db_requester.models import AccountTransactionTemplate
from utils.data_generator import DataGenerator

class TestOtherApi:
    def test_accounts_transaction_template_insufficient_funds(self, db_session: Session):
        # ======================================================================
        # Подготовка к тесту: создаём записи с начальными балансами
        stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=100)
        bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)

        db_session.add_all([stan, bob])
        db_session.commit()

        def transfer_money(session, from_account, to_account, amount):
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account: Идентификатор (user) счета, с которого списываются деньги.
            :param to_account: Идентификатор (user) счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            # Получаем счета из базы
            from_acc = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
            to_acc = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            # Проверяем, что на счете достаточно средств
            if from_acc.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            # Если средств достаточно, выполняем перевод
            from_acc.balance -= amount
            to_acc.balance += amount
            session.commit()

        # ======================================================================
        # Тест: проверяем начальные балансы
        assert stan.balance == 100
        assert bob.balance == 500

        # Пытаемся выполнить перевод 200 единиц от stan к bob,
        # но у Стэна недостаточно средств.
        with pytest.raises(ValueError, match="Недостаточно средств на счете"):
            transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

        # Откатываем изменения (если они были) и обновляем объекты из базы
        db_session.rollback()
        db_session.refresh(stan)
        db_session.refresh(bob)

        # Проверяем, что балансы не изменились
        assert stan.balance == 100
        assert bob.balance == 500

        # ======================================================================
        # Чистим данные из базы
        db_session.delete(stan)
        db_session.delete(bob)
        db_session.commit()
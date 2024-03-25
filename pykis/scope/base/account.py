from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION_CONDITION,
    ORDER_PRICE,
)
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base.market import KisMarketScope
from pykis.scope.base.product import KisProductScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccountScope(KisMarketScope):
    """한국투자증권 계좌 Base Scope"""

    account_number: KisAccountNumber | None
    """Scope에서 사용할 계좌 정보"""

    def __init__(
        self, kis: "PyKis", market: MARKET_TYPE | None = None, account: KisAccountNumber | None = None
    ):
        super().__init__(
            kis=kis,
            market=market,
        )
        self.account_number = account

    @property
    def account(self) -> KisAccountNumber:
        """
        계좌 정보를 반환합니다. 스코프에 계좌 정보가 없는 경우 기본 계좌 정보를 반환합니다.

        Raises:
            ValueError: 스코프에 계좌 정보가 없으며, 기본 계좌 정보가 없을 경우
        """
        if self.account_number is None:
            return self.kis.primary

        return self.account_number

    def orderable_amount(
        self,
        code: "str | KisProductScope",
        market: MARKET_TYPE | None = None,
        price: ORDER_PRICE | None = None,
        condition: ORDER_CONDITION | None = None,
        execution: ORDER_EXECUTION_CONDITION | None = None,
    ):
        """
        한국투자증권 주문가능금액 조회

        국내주식주문 -> 매수가능조회[v1_국내주식-007]
        해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

        Args:
            code (str | KisProductScope): 종목코드 또는 종목
            market (MARKET_TYPE | None, optional): 시장구분. None인 경우 종목코드에서 추출
            price (ORDER_PRICE | None, optional): 주문가격. None인 경우 시장가 주문
            condition (ORDER_CONDITION | None, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION | None, optional): 채결조건
            account (str | KisAccountNumber | None, optional): 계좌번호. None인 경우 기본 계좌 사용

        Examples:
            >>> account.orderable_amount(stock, price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> account.orderable_amount(stock, price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> account.orderable_amount(stock, price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
            >>> account.orderable_amount(stock, price=100, condition='best', execution=None) # 국내 최유리지정가 매수
            >>> account.orderable_amount(stock, price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
            >>> account.orderable_amount(stock, price=100, condition='extended', execution=None) # 국내 시간외단일가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='before', execution=None) # 국내 장전시간외 매수
            >>> account.orderable_amount(stock, price=None, condition='after', execution=None) # 국내 장후시간외 매수
            >>> account.orderable_amount(stock, price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> account.orderable_amount(stock, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
            >>> account.orderable_amount(stock, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
            >>> account.orderable_amount(stock, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
            >>> account.orderable_amount(stock, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
            >>> account.orderable_amount(stock, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
            >>> account.orderable_amount(stock, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 주문조건이 잘못된 경우
        """
        from pykis.api.account.orderable_amount import orderable_amount
        from pykis.api.stock.info import resolve_market

        if isinstance(code, KisProductScope):
            market = code.market
            code = code.code

        market = market or self.market

        if not market:
            market = resolve_market(self.kis, code)

        return orderable_amount(
            self.kis,
            account=self.account,
            market=market,
            code=code,
            price=price,
            condition=condition,
            execution=execution,
        )

class DomainError(Exception):
    """Erro da camada de domínio."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class BusinessRuleError(DomainError):
    pass


# ADR-002: Сбработка ошибок
Дата: 2025-10-22
Статус: Accepted

## Context
В текущей реализации ошибки возвращаются в разном формате. Нужен единый стандарт для:
- Лучшего UX
- Упрощения отладки
- Соответствия best practices

## Decision
Принять единый формат:
```json
{
  "type": "https://example.com/errors/validation",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Title exceeds maximum length",
  "instance": "/suggestions/"
}

## Consequences
### Positive
- Стандартизированный формат
- Упрощение клиентской логики
- Лучшая документированность


## Links
- NFR-007 (Аудит действий)
- Tests: `test_error_format`

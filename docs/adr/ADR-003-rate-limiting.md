# ADR-003: Rate Limiting
Дата: 2025-10-22
Статус: Accepted

## Context
API подвержено DDoS атакам и злоупотреблениям. Нужно защитить от:
- Брутфорс атак
- Исчерпания ресурсов
- Непреднамеренной перегрузки

## Decision
Внедрить Rate Limiting на уровне приложения:
- 10 запросов в минуту на пользователя (по user_id)
- 100 запросов в минуту общий лимит

## Consequences
### Positive
- Защита от DDoS
- Справедливое распределение ресурсов

### Negative    
- Дополнительная сложность
- Возможные false-positive 


## Links
- NFR-004 (Rate limiting)
- F1 (Пользователь → FastAPI)
- Tests: `test_rate_limiting`

# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [ ] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [ ] Backup cũng phải ở trong lãnh thổ VN
- [ ] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [ ] Thu thập consent trước khi dùng data cho AI training
- [ ] Có mechanism để user rút consent (Right to Erasure)
- [ ] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [ ] Có incident response plan
- [ ] Alert tự động khi phát hiện breach
- [ ] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [ ] Đã bổ nhiệm Data Protection Officer
- [ ] DPO có thể liên hệ tại: ___

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | Envelope Encryption (AES-256-GCM) | ✅ Done | Infra Team |
| Audit logging | FastAPI Middleware + CSV Audit Trail | ✅ Done | Platform Team |
| Breach detection | Prometheus + Grafana Anomaly Alerts | ✅ Done | Security Team |

## F. Technical Solutions Implemented
- **Audit Logging**: Implemented a custom FastAPI middleware that logs every request's metadata (user, path, status, timestamp) to `data/audit_logs.csv`. This provides a permanent trail for compliance audits.
- **Breach Detection**: Instrumented the API with `prometheus-fastapi-instrumentator`. Security events like unauthorized access (403 errors) are tracked, allowing Prometheus to trigger alerts when anomaly thresholds are met.
- **Encryption**: Built a `SimpleVault` using the Envelope Encryption pattern. Data Keys (DEK) are protected by a Master Key (KEK), and data is encrypted using AES-256-GCM at rest.
- **Data Minimization**: Integrated Microsoft Presidio with a custom Vietnamese `vi_core_news_lg` model to ensure all PII is anonymized before being used for AI training.

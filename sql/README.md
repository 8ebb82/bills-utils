## 转为 SQL 语句 (MySQL)

### 支付宝账单

```bash
python sql/alipay_bills_to_sql.py --source-dir /path/to/bills --output alipay_bills_all.sql --table-name alipay_bills
```

### 微信账单

```bash
python sql/wx_bills_to_sql.py --source-dir /path/to/bills --output wechat_bills_all.sql --table-name wechat_bills
```
import pandas as pd
import os
import glob
import argparse
from csv_encoding import detect_csv_encoding


def clean_sql_value(val):
    if pd.isna(val):
        return ""
    return str(val).replace("'", "''").strip()


def process_alipay_csv(file_path):
    """专门解析支付宝CSV格式：寻找表头并清洗数据"""
    try:
        enc, header_index = detect_csv_encoding(file_path)

        df = pd.read_csv(
            file_path,
            encoding=enc,
            skiprows=header_index,
            on_bad_lines="skip",
        )

        df.columns = [c.strip() for c in df.columns]

        mapping = {
            "交易时间": "transaction_time",
            "交易分类": "category",
            "交易对方": "counterparty",
            "对方账号": "counterparty_account",
            "商品说明": "product_name",
            "收/支": "direction",
            "金额": "amount",
            "收/付款方式": "payment_method",
            "交易状态": "status",
            "交易订单号": "transaction_id",
            "商家订单号": "merchant_id",
            "备注": "remark",
        }

        df = df[list(mapping.keys())].copy()
        df.columns = [mapping[c] for c in df.columns]

        df["transaction_id"] = df["transaction_id"].astype(str).str.strip()
        df["merchant_id"] = df["merchant_id"].astype(str).str.strip()

        df["amount"] = pd.to_numeric(
            df["amount"].astype(str).str.replace(",", ""), errors="coerce"
        )

        df = df.dropna(subset=["transaction_id", "amount"])

        return df

    except Exception as e:
        print(f"解析文件 {file_path} 出错: {e}")
        return None


def run_batch(source_dir, output_sql, table_name):
    all_files = glob.glob(os.path.join(source_dir, "*.csv"))
    print(f"找到 {len(all_files)} 个支付宝 CSV 文件待处理...")

    with open(output_sql, "w", encoding="utf-8") as f_out:
        for file_path in all_files:
            print(f"正在处理: {os.path.basename(file_path)}...")
            df = process_alipay_csv(file_path)

            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    sql = (
                        f"INSERT INTO {table_name} (transaction_time, category, counterparty, "
                        f"counterparty_account, product_name, direction, amount, payment_method, "
                        f"status, transaction_id, merchant_id, remark) VALUES ("
                        f"'{clean_sql_value(row['transaction_time'])}', '{clean_sql_value(row['category'])}', '{clean_sql_value(row['counterparty'])}', "
                        f"'{clean_sql_value(row['counterparty_account'])}', '{clean_sql_value(row['product_name'])}', '{clean_sql_value(row['direction'])}', "
                        f"{row['amount']}, '{clean_sql_value(row['payment_method'])}', '{clean_sql_value(row['status'])}', "
                        f"'{clean_sql_value(row['transaction_id'])}', '{clean_sql_value(row['merchant_id'])}', '{clean_sql_value(row['remark'])}');\n"
                    )
                    f_out.write(sql)

    print(f"\n全部完成！生成的 SQL 文件：{output_sql}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--table-name", required=True)
    args = parser.parse_args()
    run_batch(args.source_dir, args.output, args.table_name)
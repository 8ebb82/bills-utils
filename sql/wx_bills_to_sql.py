import pandas as pd
import os
import glob
import argparse


def clean_sql_value(val):
    if pd.isna(val):
        return ""
    return str(val).replace("'", "''").strip()


def process_file(file_path):
    """鲁棒性读取并定位真实数据起始行"""
    try:
        df_raw = pd.read_excel(file_path, engine="openpyxl", header=None)
    except Exception:
        try:
            df_raw = pd.read_csv(file_path, header=None, encoding="utf-8")
        except Exception:
            df_raw = pd.read_csv(file_path, header=None, encoding="gb18030")

    header_row_index = None
    for i, row in df_raw.iterrows():
        if "交易单号" in str(row.values):
            header_row_index = i
            break

    if header_row_index is None:
        print(f"跳过：文件 {file_path} 未能识别到交易记录表头")
        return None

    df = df_raw.iloc[header_row_index + 1 :].copy()
    df.columns = [
        "transaction_id",
        "transaction_time",
        "transaction_type",
        "direction",
        "payment_method",
        "amount",
        "counterparty",
        "merchant_id",
    ]

    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("¥", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    df = df.dropna(subset=["transaction_id"])
    return df


def run_batch(source_dir, output_sql, table_name):
    all_files = [
        f
        for f in glob.glob(os.path.join(source_dir, "*.xlsx"))
        if not os.path.basename(f).startswith(".~")
    ]

    print(f"找到 {len(all_files)} 个有效文件待处理...")

    with open(output_sql, "w", encoding="utf-8") as f_out:
        for file_path in all_files:
            print(f"正在处理: {os.path.basename(file_path)}...")
            df = process_file(file_path)

            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    sql = (
                        f"INSERT INTO {table_name} (transaction_id, transaction_time, transaction_type, "
                        f"direction, payment_method, amount, counterparty, merchant_id) VALUES ("
                        f"'{clean_sql_value(row['transaction_id'])}', '{clean_sql_value(row['transaction_time'])}', "
                        f"'{clean_sql_value(row['transaction_type'])}', '{clean_sql_value(row['direction'])}', "
                        f"'{clean_sql_value(row['payment_method'])}', {row['amount']}, "
                        f"'{clean_sql_value(row['counterparty'])}', '{clean_sql_value(row['merchant_id'])}');\n"
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
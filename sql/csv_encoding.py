def detect_csv_encoding(file_path):
    encodings = ["gb18030", "utf-8"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                lines = f.readlines()
        except (UnicodeDecodeError, UnicodeError):
            continue
        for i, line in enumerate(lines):
            if "交易时间" in line and "交易订单号" in line:
                return (enc, i)
    raise ValueError(f"无法识别文件 {file_path} 的编码格式或未找到支付宝标准表头")
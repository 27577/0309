def download_table(table_name):
    engine = db.get_engine()
    df = pd.read_sql_table(table_name, con=engine)

    # 将 DataFrame 转换为 CSV 格式的字符串，然后发送给客户端
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name=f"{table_name}.csv", mimetype='text/csv')
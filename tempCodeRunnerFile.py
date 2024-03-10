@app.route('/repo_igni')
def repo_igni():
    engine = db.get_engine()
    with engine.connect() as conn:
        sql_query = text("""
            select
                ps_partkey,
                sum(ps_supplycost * ps_availqty) as value
            from
                partsupp,
                supplier,
                nation
            where
                ps_suppkey = s_suppkey
                and s_nationkey = n_nationkey
                and n_name = 'GERMANY'
            group by
                ps_partkey having
                    sum(ps_supplycost * ps_availqty) > (
                        select
                            sum(ps_supplycost * ps_availqty) * 0.0001000000
                        from
                            partsupp,
                            supplier,
                            nation
                        where
                            ps_suppkey = s_suppkey
                            and s_nationkey = n_nationkey
                            and n_name = 'GERMANY'
                    )
            order by
                value desc;

        """)
        result = conn.execute(sql_query).fetchall()
    return render_template('repo_igni.html', results=result)
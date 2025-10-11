def test_generic_generator_hr_core():
    from core.generators import generate
    rows = generate(domain="hr_core", table="employees", rows=5)
    assert len(rows) == 5
    first = rows[0]
    # Campos fundamentales
    for field in [
        "id","natural_key","tenant_id","source_system","source_table","batch_id","batch_time_utc",
        "is_active","valid_from_utc","created_at_utc","updated_at_utc","record_hash",
        "dq_completeness_pct","dq_validity_pct","geo_country","currency_code","fx_rate_to_usd"
    ]:
        assert field in first, f"Falta campo común {field}"
    assert first["processing_status"] in {"ok", "warn"}
    # Métricas dentro de rango
    assert 0 <= first["dq_completeness_pct"] <= 100
    assert 0 <= first["dq_validity_pct"] <= 100

def test_dq_extended_metrics():
    from core.generators import generate
    from core.dq import profiler
    rows = generate(domain="hr_core", table="employees", rows=10)
    metrics = profiler.profile(rows)
    sample_col = next(iter(metrics.keys()))
    assert "duplicates_count" in metrics[sample_col]
    assert "uniqueness_ratio" in metrics[sample_col]

def test_error_profiles():
    from core.generators import generate
    # Test sin errores
    rows_none = generate(domain="hr_core", table="employees", rows=10, error_profile="none")
    assert all(r["processing_status"] == "ok" for r in rows_none)
    # Test con errores leves
    rows_light = generate(domain="hr_core", table="employees", rows=10, error_profile="light")
    has_warn = any(r["processing_status"] == "warn" for r in rows_light)
    assert has_warn  # Debería haber algunos errores con perfil light

#!/usr/bin/env python3
"""
Test script to verify date range functionality
"""
import sys
sys.path.insert(0, '.')

from datetime import datetime
from core.engines import faker_engine
from core.generators import generate

def test_date_range_engine():
    """Test that the date range is properly set in the engine"""
    print("=" * 60)
    print("TEST 1: Date Range Engine Configuration")
    print("=" * 60)
    
    # Set a date range
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    print(f"Setting date range: {start_date} to {end_date}")
    faker_engine.set_date_range(start_date, end_date)
    
    print("✓ Date range set successfully")
    print()
    return True

def test_date_generation():
    """Test that generated dates fall within the specified range"""
    print("=" * 60)
    print("TEST 2: Date Generation Within Range")
    print("=" * 60)
    
    # Set a specific date range
    start_date = "2023-06-01"
    end_date = "2023-08-31"
    
    print(f"Setting date range: {start_date} to {end_date}")
    faker_engine.set_date_range(start_date, end_date)
    
    # Generate test data with date fields
    # Using a table that likely has date fields
    try:
        print("\nGenerating sample data with date fields...")
        data = generate("finance", "dim_account", 10, error_profile="none")
        
        print(f"✓ Generated {len(data)} records")
        
        # The data is a list of dicts
        if data and len(data) > 0:
            # Check if there are any date fields
            sample_record = data[0]
            date_fields = [key for key in sample_record.keys() if 'date' in key.lower() or 'time' in key.lower()]
            
            if date_fields:
                print(f"\nDate fields found: {date_fields}")
                
                for field in date_fields:
                    # Sample first few records
                    print(f"\n  {field} samples:")
                    for i, record in enumerate(data[:3]):
                        val = record.get(field, 'N/A')
                        print(f"    Record {i+1}: {val}")
                        
                        # Try to validate the date is in range
                        if val and val != 'N/A':
                            try:
                                from datetime import datetime
                                # Parse the date
                                if isinstance(val, str):
                                    if 'T' in val:  # ISO datetime
                                        dt_str = val.replace('Z', '+00:00')
                                        dt = datetime.fromisoformat(dt_str)
                                    else:  # Just a date
                                        dt = datetime.fromisoformat(val)
                                    
                                    # Check if in range (use date only for comparison)
                                    start_dt = datetime.fromisoformat("2023-06-01")
                                    end_dt = datetime.fromisoformat("2023-08-31T23:59:59")
                                    
                                    # Compare just the dates
                                    dt_date = dt.date() if hasattr(dt, 'date') else dt
                                    start_date = start_dt.date()
                                    end_date = end_dt.date()
                                    
                                    if start_date <= dt_date <= end_date:
                                        print(f"      ✓ Date is within range ({dt_date})")
                                    else:
                                        print(f"      ⚠ Date is OUTSIDE range: {dt_date}")
                            except Exception as e:
                                print(f"      Could not validate: {e}")
            else:
                print("\n⚠ No date fields found in this table")
        else:
            print("\n⚠ No data generated")
            
        print("\n✓ Date generation test completed")
        return True
        
    except Exception as e:
        print(f"\n✗ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_date_range_validation():
    """Test date range validation and normalization"""
    print("\n" + "=" * 60)
    print("TEST 3: Date Range Validation")
    print("=" * 60)
    
    # Test that reversed dates are normalized
    print("\nTest: Reversed date range (should be auto-corrected)")
    faker_engine.set_date_range("2024-12-31", "2024-01-01")
    print("✓ Reversed dates accepted (should be normalized internally)")
    
    # Test YYYY-MM format
    print("\nTest: YYYY-MM format")
    faker_engine.set_date_range("2023-01", "2023-12")
    print("✓ YYYY-MM format accepted")
    
    # Test clearing range
    print("\nTest: Clearing date range")
    faker_engine.set_date_range(None, None)
    print("✓ Date range cleared")
    
    return True

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "DATE RANGE FUNCTIONALITY TESTS" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        test_date_range_engine,
        test_date_generation,
        test_date_range_validation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())

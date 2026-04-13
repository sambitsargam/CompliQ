# Sample Docs For CompliQ Testing

Use these files in `/dashboard` upload flow to test different compliance outcomes.

## Files

1. `01_weak_policy.txt`
- Expected: many gaps (about 5 findings)
- Expected trend: low coverage, high risk

2. `02_basic_operations_policy.md`
- Contains ownership + review keywords
- Expected: partial coverage, medium risk

3. `03_security_controls_policy.md`
- Contains ownership + review + access keywords
- Expected: fewer gaps than basic policy

4. `04_incident_playbook_note.txt`
- Contains incident keywords but misses governance sections
- Expected: mixed results with multiple gaps

5. `05_comprehensive_policy.md`
- Contains all primary control keywords
- Expected: highest coverage, lowest risk

## Fast Test Plan

1. Upload only `01_weak_policy.txt` and run analysis.
2. Upload only `05_comprehensive_policy.md` and run analysis.
3. Compare coverage and risk values.
4. Upload `01` + `05` together and run analysis to see combined behavior.

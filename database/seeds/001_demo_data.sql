-- Seed Data for MindSafe

TRUNCATE TABLE consent_logs, notifications, case_notes, hearings, alerts, check_in_domains, check_ins, cases, users, counsellors RESTART IDENTITY CASCADE;

-- Counsellor
INSERT INTO counsellors (id, email, password_hash, name, title, city) VALUES 
('00000000-0000-0000-0000-000000000001', 'dr.meera.iyer@wcd.gov.in', '$2a$10$abcdefghijklmnopqrstuv', 'Dr. Meera Iyer', 'Senior Counsellor', 'Mumbai');

-- Users
INSERT INTO users (id, phone, name, age, language) VALUES 
('11111111-1111-1111-1111-111111111111', '+919876543210', 'Priya Sharma', 28, 'English'),
('22222222-2222-2222-2222-222222222222', '+919876543211', 'Kavitha Reddy', 34, 'Telugu'),
('33333333-3333-3333-3333-333333333333', '+919876543212', 'Lakshmi Patel', 22, 'Tamil'),
('44444444-4444-4444-4444-444444444444', '+919876543213', 'Sunita Devi', 45, 'Hindi'),
('55555555-5555-5555-5555-555555555555', '+919876543214', 'Anjali Bose', 31, 'Bengali'),
('66666666-6666-6666-6666-666666666666', '+919876543215', 'Rekha Gupta', 38, 'Hindi');

-- Cases
INSERT INTO cases (id, case_number, victim_id, counsellor_id, case_type, court, risk_score, risk_level, status, city, next_hearing_date, streak, total_sessions, trend) VALUES 
('c1111111-1111-1111-1111-111111111111', 'MH-2026-0041', '11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000001', 'Domestic Violence', 'Family Court Mumbai', 78, 'high', 'active', 'Mumbai', '2026-09-18', 12, 34, 'worsening'),
('c2222222-2222-2222-2222-222222222222', 'MH-2026-0028', '22222222-2222-2222-2222-222222222222', '00000000-0000-0000-0000-000000000001', 'Sexual Violence', NULL, 41, 'moderate', 'active', 'Bengaluru', '2026-09-25', 0, 0, 'improving'),
('c3333333-3333-3333-3333-333333333333', 'MH-2026-0015', '33333333-3333-3333-3333-333333333333', '00000000-0000-0000-0000-000000000001', 'Domestic Violence', NULL, 92, 'critical', 'active', 'Chennai', '2026-09-10', 0, 0, 'worsening'),
('c4444444-4444-4444-4444-444444444444', 'MH-2026-0037', '44444444-4444-4444-4444-444444444444', '00000000-0000-0000-0000-000000000001', 'Harassment', NULL, 23, 'stable', 'monitoring', 'Jaipur', '2026-10-02', 0, 0, 'stable'),
('c5555555-5555-5555-5555-555555555555', 'MH-2026-0043', '55555555-5555-5555-5555-555555555555', '00000000-0000-0000-0000-000000000001', 'Domestic Violence', NULL, 65, 'moderate', 'active', 'Kolkata', '2026-09-22', 0, 0, 'worsening'),
('c6666666-6666-6666-6666-666666666666', 'MH-2026-0051', '66666666-6666-6666-6666-666666666666', '00000000-0000-0000-0000-000000000001', 'Sexual Violence', NULL, 55, 'moderate', 'active', 'Lucknow', '2026-09-30', 0, 0, 'stable');

-- Update Users case_id
UPDATE users SET case_id = 'c1111111-1111-1111-1111-111111111111' WHERE id = '11111111-1111-1111-1111-111111111111';
UPDATE users SET case_id = 'c2222222-2222-2222-2222-222222222222' WHERE id = '22222222-2222-2222-2222-222222222222';
UPDATE users SET case_id = 'c3333333-3333-3333-3333-333333333333' WHERE id = '33333333-3333-3333-3333-333333333333';
UPDATE users SET case_id = 'c4444444-4444-4444-4444-444444444444' WHERE id = '44444444-4444-4444-4444-444444444444';
UPDATE users SET case_id = 'c5555555-5555-5555-5555-555555555555' WHERE id = '55555555-5555-5555-5555-555555555555';
UPDATE users SET case_id = 'c6666666-6666-6666-6666-666666666666' WHERE id = '66666666-6666-6666-6666-666666666666';

-- Alerts
INSERT INTO alerts (id, case_id, severity, type, title, message, is_resolved) VALUES 
('a0010000-0000-0000-0000-000000000000', 'c3333333-3333-3333-3333-333333333333', 'critical', 'Distress Spike', 'Distress Spike Detected', 'Distress Spike Detected — Lakshmi, critical, surged 68→92', false),
('a0020000-0000-0000-0000-000000000000', 'c1111111-1111-1111-1111-111111111111', 'high', 'Missed Check-in', 'Missed Check-in', 'Missed Check-in — Priya, high, 2 days missed', false),
('a0030000-0000-0000-0000-000000000000', 'c5555555-5555-5555-5555-555555555555', 'moderate', 'Trend Decline', 'Trend Decline', 'Trend Decline — Anjali, moderate, 7-day score +18', false),
('a0040000-0000-0000-0000-000000000000', 'c6666666-6666-6666-6666-666666666666', 'moderate', 'Pre-hearing Anxiety', 'Pre-hearing Anxiety', 'Pre-hearing Anxiety — Rekha, moderate, hearing in 5 days', false),
('a0050000-0000-0000-0000-000000000000', 'c2222222-2222-2222-2222-222222222222', 'low', 'Routine Reminder', 'Routine Reminder', 'Routine Reminder — Kavitha, low, overdue 6h', true);

-- Hearings
INSERT INTO hearings (case_id, hearing_date, hearing_type) VALUES 
('c1111111-1111-1111-1111-111111111111', '2026-09-18', 'Standard'),
('c2222222-2222-2222-2222-222222222222', '2026-09-25', 'Standard'),
('c3333333-3333-3333-3333-333333333333', '2026-09-10', 'Standard'),
('c4444444-4444-4444-4444-444444444444', '2026-10-02', 'Standard'),
('c5555555-5555-5555-5555-555555555555', '2026-09-22', 'Standard'),
('c6666666-6666-6666-6666-666666666666', '2026-09-30', 'Standard');

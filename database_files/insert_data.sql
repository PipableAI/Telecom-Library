INSERT INTO user_details (user_id, first_name, last_name, email_id, slack_member_id)
VALUES
    ('A1', 'Rohan', 'Bhatiyal', 'rohan@pipable.ai', 'U05K8B785E3'),
    ('A2', 'Pratham', 'Gupta', 'pratham@pipable.ai', 'U05KR7LH32Q'),
    ('A3', 'Soham', 'Acharya', 'soham@pipable.ai', 'U05KNS96CR0'),
    ('A4', 'Avi', 'Kothari', 'avi@pipable.ai', 'U05TYQ9D17S'),
    ('A5', 'Ritvik', 'Kalra', 'ritvik@pipable.ai', 'U05KGDU7AS2');

INSERT INTO baseband_info (site_id, baseband_serial, baseband_type, cm_profile, site_manager)
VALUES
    ('14881_Lala_Land_River', 'ABC123XYZ789456P', 'DUX3423', '1234567890.prf', 'A1'),
    ('14884_Lala_Land_Valley', 'DEF456LMN123789Q', 'DUX3163', '9876543210.prf', 'A2'),
    ('14885_Lala_Land_Mountain', 'GHI789UVW456123R', 'DUX3365', '3456789012.prf', 'A3'),
    ('14883_Lala_Land_Hilltop', 'JKL012XYZ789456S', 'DUX3463', '3112444afb684572.prf', 'A4'),
    ('14887_Lala_Land_Forest', 'MNO345ABC678912T', 'DUX3161', '2345678901.prf', 'A5');

INSERT INTO cm_policy (baseband_type, cm_profile)
VALUES
    ('DUX3423', '1234567890.prf'),
    ('DUX3163', '9876543210.prf'),
    ('DUX3365', '3456789012.prf'),
    ('DUX3463', 'db96118c24d39e02.prf'),
    ('DUX3161', '2345678901.prf');

INSERT INTO events (event_timestamp, event_id, event_detail)
VALUES
    ('2024-01-16 12:30:00', 'INC0010003', 'Baseband replacement');

INSERT INTO site_events (site_id, event_id)
VALUES
    ('14883_Lala_Land_Hilltop', 'INC0010003');
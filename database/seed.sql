-- Project: SmartServe (Sample Data)
-- Description: Seed Data for Barangay Document Management System (Testing Purposes)

-- ==========================================
-- 1. SAMPLE RESIDENTS
-- Passwords are placeholders for testing
-- ==========================================
INSERT INTO user (username, email, password, role, first_name, last_name, phone, address) VALUES 
('juan_delacruz', 'juan@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Juan', 'Dela Cruz', '09171234567', 'Purok 1, Batangas City'),
('maria_clara', 'maria@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Maria', 'Clara', '09171234568', 'Purok 2, Batangas City'),
('jose_rizal', 'jose@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Jose', 'Rizal', '09171234569', 'Purok 3, Batangas City'),
('andres_boni', 'andres@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Andres', 'Bonifacio', '09171234570', 'Purok 4, Batangas City'),
('emilio_aguinaldo', 'emilio@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Emilio', 'Aguinaldo', '09171234571', 'Purok 5, Batangas City'),
('apolinario_mabini', 'pol@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Apolinario', 'Mabini', '09171234572', 'Purok 6, Batangas City'),
('antonio_luna', 'luna@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Antonio', 'Luna', '09171234573', 'Purok 1, Batangas City'),
('gregorio_delpilar', 'goyo@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Gregorio', 'Del Pilar', '09171234574', 'Purok 2, Batangas City'),
('gabriela_silang', 'gabriela@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Gabriela', 'Silang', '09171234575', 'Purok 3, Batangas City'),
('melchora_aquino', 'tandang_sora@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Melchora', 'Aquino', '09171234576', 'Purok 4, Batangas City'),
('lapu_lapu', 'lapu@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Lapu', 'Lapu', '09171234577', 'Purok 5, Batangas City'),
('francisco_balagtas', 'kiko@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Francisco', 'Balagtas', '09171234578', 'Purok 6, Batangas City'),
('marcelo_delpilar', 'marcelo@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Marcelo', 'Del Pilar', '09171234579', 'Purok 1, Batangas City'),
('graciano_lopez', 'graciano@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Graciano', 'Lopez Jaena', '09171234580', 'Purok 2, Batangas City'),
('juan_luna', 'juanluna@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Juan', 'Luna', '09171234581', 'Purok 3, Batangas City'),
('mariano_gomez', 'gomez@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Mariano', 'Gomez', '09171234582', 'Purok 4, Batangas City'),
('jose_burgos', 'burgos@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Jose', 'Burgos', '09171234583', 'Purok 5, Batangas City'),
('jacinto_zamora', 'zamora@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Jacinto', 'Zamora', '09171234584', 'Purok 6, Batangas City'),
('emilio_jacinto', 'dimasalang@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Emilio', 'Jacinto', '09171234585', 'Purok 1, Batangas City'),
('miguel_malvar', 'malvar@gmail.com', 'scrypt:32768:8:1$DummyHash...', 'resident', 'Miguel', 'Malvar', '09171234586', 'Purok 2, Batangas City');

-- ==========================================
-- 2. SAMPLE REQUESTS
-- Linked to User IDs above
-- ==========================================
INSERT INTO request (user_id, document_type, description, status) VALUES
(1, 'barangay_clearance', 'For employment purposes', 'pending'),
(2, 'residency_cert', 'Proof of residency for bank', 'approved'),
(3, 'indigency_cert', 'Scholarship application', 'pending'),
(4, 'barangay_clearance', 'Business permit renewal', 'completed'),
(5, 'business_permit', 'Sari-sari store application', 'rejected'),
(1, 'residency_cert', 'Voters registration', 'approved'),
(2, 'barangay_clearance', 'Job application requirement', 'pending'),
(3, 'indigency_cert', 'Medical assistance', 'completed'),
(6, 'barangay_clearance', 'New work requirement', 'pending'),
(7, 'residency_cert', 'Postal ID application', 'approved'),
(8, 'indigency_cert', 'School requirement', 'pending'),
(9, 'barangay_clearance', 'Travel requirement', 'completed'),
(10, 'business_permit', 'Small eatery permit', 'rejected'),
(11, 'barangay_clearance', 'Local employment', 'approved'),
(12, 'residency_cert', 'Bank account opening', 'pending'),
(13, 'indigency_cert', 'Financial aid request', 'completed'),
(14, 'barangay_clearance', 'Work permit', 'pending'),
(15, 'residency_cert', 'ID application', 'approved'),
(16, 'indigency_cert', 'School scholarship', 'pending'),
(17, 'barangay_clearance', 'Driver license requirement', 'completed');
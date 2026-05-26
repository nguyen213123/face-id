-- Database schema for ProjectPython-FaceID
-- MySQL script: creates database and tables expected by the Python DAL
CREATE DATABASE IF NOT EXISTS `quanlysinhvien` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
USE `quanlysinhvien`;

-- Table: lop
CREATE TABLE IF NOT EXISTS `lop` (
  `malop` VARCHAR(20) NOT NULL,
  `tenlop` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`malop`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: quyen
CREATE TABLE IF NOT EXISTS `quyen` (
  `maquyen` VARCHAR(20) NOT NULL,
  `tenquyen` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`maquyen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: chucnang
CREATE TABLE IF NOT EXISTS `chucnang` (
  `machucnang` VARCHAR(20) NOT NULL,
  `tenchucnang` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`machucnang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Mapping table: quyen_chucnang
CREATE TABLE IF NOT EXISTS `quyen_chucnang` (
  `maquyen` VARCHAR(20) NOT NULL,
  `machucnang` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`maquyen`, `machucnang`),
  FOREIGN KEY (`maquyen`) REFERENCES `quyen`(`maquyen`) ON DELETE CASCADE,
  FOREIGN KEY (`machucnang`) REFERENCES `chucnang`(`machucnang`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: taikhoan
CREATE TABLE IF NOT EXISTS `taikhoan` (
  `mataikhoan` VARCHAR(20) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `matkhau` VARCHAR(255) DEFAULT NULL,
  `maquyen` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`mataikhoan`),
  UNIQUE KEY `uq_taikhoan_email` (`email`),
  FOREIGN KEY (`maquyen`) REFERENCES `quyen`(`maquyen`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: sinhvien
CREATE TABLE IF NOT EXISTS `sinhvien` (
  `masinhvien` VARCHAR(20) NOT NULL,
  `hoten` VARCHAR(255) DEFAULT NULL,
  `malop` VARCHAR(20) DEFAULT NULL,
  `cmnd` VARCHAR(50) DEFAULT NULL,
  `gioitinh` VARCHAR(20) DEFAULT NULL,
  `ngaysinh` DATE DEFAULT NULL,
  `email` VARCHAR(255) DEFAULT NULL,
  `sodienthoai` VARCHAR(50) DEFAULT NULL,
  `khoahoc` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`masinhvien`),
  FOREIGN KEY (`malop`) REFERENCES `lop`(`malop`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: hinhanh_sinhvien
CREATE TABLE IF NOT EXISTS `hinhanh_sinhvien` (
  `masinhvien` VARCHAR(20) NOT NULL,
  `hinhanh` TEXT,
  PRIMARY KEY (`masinhvien`),
  FOREIGN KEY (`masinhvien`) REFERENCES `sinhvien`(`masinhvien`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: giangvien
CREATE TABLE IF NOT EXISTS `giangvien` (
  `magiangvien` VARCHAR(20) NOT NULL,
  `hoten` VARCHAR(255) DEFAULT NULL,
  `sodienthoai` VARCHAR(50) DEFAULT NULL,
  `mataikhoan` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`magiangvien`),
  FOREIGN KEY (`mataikhoan`) REFERENCES `taikhoan`(`mataikhoan`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: buoihoc
CREATE TABLE IF NOT EXISTS `buoihoc` (
  `mabuoihoc` VARCHAR(20) NOT NULL,
  `giobatdau` TIME DEFAULT NULL,
  `gioketthuc` TIME DEFAULT NULL,
  `ngay` DATE DEFAULT NULL,
  `malop` VARCHAR(20) DEFAULT NULL,
  `magiangvien` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`mabuoihoc`),
  FOREIGN KEY (`malop`) REFERENCES `lop`(`malop`) ON DELETE SET NULL,
  FOREIGN KEY (`magiangvien`) REFERENCES `giangvien`(`magiangvien`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: diemdanh
CREATE TABLE IF NOT EXISTS `diemdanh` (
  `madiemdanh` VARCHAR(20) NOT NULL,
  `masinhvien` VARCHAR(20) DEFAULT NULL,
  `giovao` DATETIME DEFAULT NULL,
  `giora` DATETIME DEFAULT NULL,
  `mabuoihoc` VARCHAR(20) DEFAULT NULL,
  `hinhanh` TEXT,
  PRIMARY KEY (`madiemdanh`),
  FOREIGN KEY (`masinhvien`) REFERENCES `sinhvien`(`masinhvien`) ON DELETE SET NULL,
  FOREIGN KEY (`mabuoihoc`) REFERENCES `buoihoc`(`mabuoihoc`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Optional: statistics or view table used by the project (ThongKe)
-- The project defines a `ThongKe` model used for reporting; not created as a persistent table here.

-- Sample initial data (optional)
INSERT IGNORE INTO `quyen` (`maquyen`, `tenquyen`) VALUES
  ('Q001', 'Administrator'),
  ('Q002', 'User');

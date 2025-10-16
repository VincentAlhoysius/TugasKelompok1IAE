# 🛍️ Marketplace API

Backend sederhana berbasis **FastAPI** yang menyediakan fitur login, update profil, dan pengelolaan item dengan autentikasi JWT.

---
## Link GDrive
https://drive.google.com/drive/folders/1SECDh5qdCgqMX48WsgFficzM4WTu9A2v?usp=sharing
## ⚙️ Setup Environment & Menjalankan Server

### 1️⃣ Buat Virtual Environment

```bash
python -m venv venv
```

Aktifkan environment:

* **Windows (PowerShell)**

  ```bash
  .\venv\Scripts\activate
  ```
* **macOS/Linux**

  ```bash
  source venv/bin/activate
  ```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Jalankan Server

```bash
uvicorn main:app --reload
```

Akses API di: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Variabel Environment

Buat file **.env** di root project (berdasarkan `.env.example`):

```
JWT_SECRET=supersecretkey123
```

---

## 📚 Daftar Endpoint

| Endpoint      | Method | Deskripsi                    | Request Body                                              | Response (contoh)                                       |
| ------------- | ------ | ---------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| `/auth/login` | POST   | Login dan dapatkan JWT token | `{ "email": "user1@example.com", "password": "pass123" }` | `{ "access_token": "<token>" }`                         |
| `/profile`    | PUT    | Update profil (butuh token)  | `{ "name": "Vincent", "email": "vincent@example.com" }`   | `{ "name": "Vincent", "email": "vincent@example.com" }` |
| `/items`      | GET    | Ambil daftar item            | —                                                         | `[ { "id": 1, "name": "Item A", "price": 10000 } ]`     |
| `/items`      | POST   | Tambah item baru             | `{ "id": 2, "name": "Item B", "price": 15000 }`           | `{ "id": 2, "name": "Item B", "price": 15000 }`         |

---

## 🧪 Contoh Pengujian

### 🔹 Menggunakan cURL (Windows / PowerShell)

#### 1. Register

```powershell
curl.exe --% -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d "{\"email\":\"user1@example.com\",\"password\":\"pass123\"}"
```
#### 2. Login

```powershell
curl.exe --% -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"user1@example.com\",\"password\":\"pass123\"}"
```

#### 3. Update Profil (dengan token hasil login)

```powershell
curl.exe --% -X PUT http://127.0.0.1:8000/profile -H "Authorization: Bearer <JWT_TOKEN_MU>" -H "Content-Type: application/json" -d "{\"name\":\"VincentA\",\"email\":\"vincent.new@example.com\"}"
```

### 🔹 Menggunakan Postman

1. Buka **Postman**.
2. Klik **Import**.
3. Pilih file **`postman_collection.json`** dari project ini.
4. Jalankan endpoint sesuai urutan (Register → Login → Update Profile → CRUD Item).

---

## ⚠️ Catatan Kendala & Asumsi

* Token JWT memiliki masa berlaku 15 menit (default di kode).
* Email dan password tidak diverifikasi dengan database (data login bersifat statis/dummy).
* Endpoint hanya untuk tujuan **belajar konsep FastAPI + JWT**, bukan sistem produksi.
* File `.env.example` berfungsi sebagai template untuk konfigurasi manual.

---

# Analysis

## 1.Describe what you think happened that caused those bad reviews during our 12.12 event and why it happened.

Menurut analisa saya hal ini bisa terjadi karena adanya race condition yaitu kondisi dimana terdapat banyak thread yang menggunakan sumberdaya yang sama dan mencoba untuk mengubah data secara bersamaan. Dalam kasus ini terjadi pada proses update jumlah stok saat proses order item. Hal ini berpengaruh terhadap jumlah stock barang didalam database.

## 2. Based on your analysis, propose a solution that will prevent the incidents from occurring again.

Solusi untuk kasus ini adalah menggunakan message queue seperti RabbitMQ atau Kafka agar bisa memproses satu persatu dibuat seperti antrian, atau bisa juga menggunakan TRANSACTION pada SQL untuk menghindari race condition.

## 3. Based on your proposed solution, build a Proof of Concept that demonstrates technically how your solution will work.

POC yang saya buat akan menggunakan TRANSACTION dalam SQL sebagai solusi untuk menghindari terjadinya race condition. Dalam pembuatan POC ini saya akan menggunakan bahasa pemograman python dengan framework FASTAPI serta library SQLALCHEMY sebagai SQL toolkit dengan database menggunakan MySQL.

# How to use POC

## Pull Source Code

```
git clone https://github.com/therafirend/evermos.git
```

## Instalasi

### Menggunakan Docker

#### Install Docker

Jika anda belum menginstall docker, dokumentasi dan cara install docker dapat dilihat pada link berikut [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

#### Run Docker Compose

Setelah menginstall docker selanjutnya dapat menjalankan command berikut untuk menjalankan aplikasi :

```
docker compose up
```

### Tanpda Docker

#### Setting Database

Sesuaikan setting nama database, nama user, password user, dan port database pada file app/database.py berikut dengan setting database MySQL anda:

```
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/fastapi_test?charset=utf8mb4"

```

#### Run Server Uvicorn

Jalankan server uvicorn dengan command berikut:

```
uvicorn app.main:app --reload
```

## Swagger UI

Fastapi menyediakan Swagger UI untuk membukanya silahkan buka url `http://localhost:8000/docs`

## Create Item

Untuk membuat item baru gunakan metode `POST` pada url `http://localhost:8000/api/v1/items`dengan contoh body

```
{
    "name":  "Item 1",
	"stock":  1000
}
```

## Get All Item

Untuk menampilkan semua data item gunakan metode `GET` pada url `http://localhost:8000/api/v1/items`

## Get One Item

Untuk menampilkan data spesifik satu item gunakan metode `GET` pada url `http://localhost:8000/api/v1/items/:id`

## Delete Item

Untuk menghapus satu data item gunakan metode `DELETE` pada url `http://localhost:8000/api/v1/items:id`

## Update Item

Untuk mengupdate nama dan stock item gunakan metode `PUT` pada url `http://localhost:8000/api/v1/items/:id`

## Update Stock Item dengan resiko race condition

Untuk mengupdate data stock item dengan resiko race condition gunakan metode `PATCH` pada url `http://localhost:8000/api/v1/items/update_stock_race/:id` dengan contoh body

```
{
	"stock":  2000
}
```

## Update Stock Item dengan pencegahan race condition

Untuk mengupdate data stock item dengan resiko race condition gunakan metode `PATCH` pada url `http://localhost:8000/api/v1/items/update_stock/:id` dengan contoh body

```
{
	"stock":  2000
}
```

## Testing Unit Race Condition

Navigasikan kedalam folder `testing`

```
cd testing
```

Sebelum testing pastikan table item pada database kosong atau truncate terlebih dahulu, setelah itu jalankan command unit testing

```
pytest -vv
```

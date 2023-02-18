# melakukan proses import pymongo
import pymongo

# membuat config koneksi untuk menghubungkan mongodb dengan python
koneksi_url = "mongodb://localhost:27017"

# membuat sebuah function yang bertugas untuk mengecek koneksi ke mongodb
def cekMongoDB() :
    client = pymongo.MongoClient(koneksi_url)
    try:
        cek = client.list_database_names()
        print(cek)
    except:
        print("database tidak terhubung")

# membuat sebuah function yang bertugas untuk create database
def createDatabase() :
    dbClient = pymongo.MongoClient(koneksi_url)
    namaDatabase = dbClient['Database_Mahasantri_New']
    namaCollection = namaDatabase['Angkatan pertama']
    value_data = namaCollection.insert_one({ 'nama':"Feirdaus", 'jurusan': "PPL" })
    print("berhasil menambahkan data")
    print(value_data)


class MongoCRUD:
    def __init__(self, data, koneksi):
        self.client = pymongo.MongoClient(koneksi)
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def readData(self):
        documents = self.collection.find()
        value = [{
            item: data[item] for item in data if item != '_id'} for data in documents]
        return value

    def createData(self, data):
        new_document = data['document']
        response = self.collection.insert_one(new_document)
        value = {
            'status' : 'berhasil',
            'document_id' : str(response.inserted_id)
        }
        return value


    #========================================================#
    #============== fungsi untuk update data ================#

    def updateData(self):
        data_awal = self.data['dataAwal']
        update_data = {
            "$set" : self.data['dataUpdate']
        }

        response = self.collection.update_one(data_awal, update_data)
        value = {
            "status" : "berhasil diupdate" if response.modified_count > 0 else "data tidak ditemukan"
        }

        print(value)

    #========================================================#

    def deleteData(self, data):
        dataHapus = data['document']
        response = self.collection.delete_one(dataHapus)
        value = {
            "status" : "berhasil diupdate" if response.deleted_count > 0 else "data tidak ditemukan"
        }

        print(value)


if __name__ == '__main__' :
    data = {
        "database" : "Database_Mahasantri_New",
        "collection" : "Angkatan pertama",

        "dataAwal" : {
            "nama" : "Aslan",
            "jurusan" : "PPL"
        },

        "dataUpdate" : {
            "nama" : "Rendi",
            "jurusan" : "DM"
        }
    }

    data_delete = {
        'document' : {
            'nama' : 'Rendi',
            'jurusan' : "DM"
        }
    }

    mongo_objek = MongoCRUD(data, koneksi_url)
    delete = mongo_objek.deleteData(data_delete)